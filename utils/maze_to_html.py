import os
import base64

def img_to_base64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def maze_to_html(maze, rows, cols, scale=2):
    """
    Converts a maze representation to an A-Frame HTML file.
    
    Generates an interactive 3D visualization of a maze using A-Frame (WebXR framework).
    The maze is rendered as 3D boxes representing walls, with a floor plane and sky.
    
    Args:
        maze: 2D array-like structure where True/1 represents walls and False/0 represents paths.
        rows: Number of rows in the maze.
        cols: Number of columns in the maze.
        scale: Scaling factor for the 3D elements. Defaults to 2.
    
    Returns:
        str: Path to the generated HTML file.
    """

    # Make directory
    os.makedirs('./HTML', exist_ok=True)

    # Images to base64:
    floor_b64 = img_to_base64('./Images/floor_stones.jpg')
    wall_b64 = img_to_base64('./Images/wall_stones.jpg')
    moon_b64 = img_to_base64('./Images/moon.jpg')
    sky_b64 = img_to_base64('./Images/sky.jpg')

    # Check whether the file exits already
    base = f'./HTML/maze_{rows}x{cols}'
    path = f'{base}.html'
    i = 1
    while os.path.exists(path):
        path = f'{base}_{i}.html'
        i += 1


    # Header of the html file
    lines = ['<html>', 
             '<head>', 
            '<script src="https://aframe.io/releases/1.7.0/aframe.min.js"></script>',
            
            # Adds physics --> The camera hits the wall
            """
            <script>
            AFRAME.registerComponent('maze-controls', {
            schema: { speed: { type: 'number', default: 5 }, size: { type: 'number', default: 0.5 } },
            init: function () {
                this.keys = {};
                this.onKeyDown = function (e) { this.keys[e.key.toLowerCase()] = true; }.bind(this);
                this.onKeyUp = function (e) { this.keys[e.key.toLowerCase()] = false; }.bind(this);
                window.addEventListener('keydown', this.onKeyDown);
                window.addEventListener('keyup', this.onKeyUp);
            },
            tick: function (t, dt) {
                if (!dt) return;
                var cam = this.el.querySelector('[camera]');
                if (!cam) return;
                var dir = new THREE.Vector3();
                cam.object3D.getWorldDirection(dir);
                dir.negate();
                dir.y = 0;
                dir.normalize();
                var right = new THREE.Vector3(-dir.z, 0, dir.x);
                var move = new THREE.Vector3();
                if (this.keys['w'] || this.keys['arrowup']) move.add(dir);
                if (this.keys['s'] || this.keys['arrowdown']) move.sub(dir);
                if (this.keys['a'] || this.keys['arrowleft']) move.sub(right);
                if (this.keys['d'] || this.keys['arrowright']) move.add(right);
                if (move.length() === 0) return;
                move.normalize();
                var spd = this.data.speed * dt / 1000;
                var pos = this.el.getAttribute('position');
                var newX = pos.x + move.x * spd;
                var newZ = pos.z + move.z * spd;
                var walls = document.querySelectorAll('.wall');
                var s = this.data.size;
                var blockedX = false, blockedZ = false;
                for (var i = 0; i < walls.length; i++) {
                var w = walls[i].object3D.position;
                var ws = parseFloat(walls[i].getAttribute('width')) / 2;
                var oX = (ws + s) - Math.abs(newX - w.x);
                var oZ = (ws + s) - Math.abs(pos.z - w.z);
                if (oX > 0 && oZ > 0) blockedX = true;
                oX = (ws + s) - Math.abs(pos.x - w.x);
                oZ = (ws + s) - Math.abs(newZ - w.z);
                if (oX > 0 && oZ > 0) blockedZ = true;
                }
                if (!blockedX) pos.x = newX;
                if (!blockedZ) pos.z = newZ;
                this.el.setAttribute('position', pos);
            },
            remove: function () {
                window.removeEventListener('keydown', this.onKeyDown);
                window.removeEventListener('keyup', this.onKeyUp);
            }
            });
            </script>
            """,
            # Toggle camera movement when T is pressed
            f"""
            <script>
            document.addEventListener('keydown', function(e) {{
            if (e.key !== 't' && e.key !== 'T') return;
            var rig = document.querySelector('#rig');
            var cam = rig.querySelector('[camera]');
            var marker = document.querySelector('#marker');
            if (!rig.dataset.aerial || rig.dataset.aerial === 'false') {{
                var p = rig.getAttribute('position');
                marker.setAttribute('position', p.x + ' ' + {scale + 0.5} + ' ' + p.z);
                marker.setAttribute('visible', true);
                rig.dataset.savedPos = JSON.stringify(rig.getAttribute('position'));
                rig.dataset.savedCamRot = JSON.stringify(cam.getAttribute('rotation'));
                cam.setAttribute('look-controls', 'enabled', false);
                cam.setAttribute('rotation', '0 0 0');
                rig.setAttribute('position', '{(maze.shape[1]-1)*scale/2} {max(maze.shape)*scale} {(maze.shape[0]-1)*scale/2}');
                rig.setAttribute('rotation', '-90 0 0');
                rig.querySelector('[maze-controls]') && rig.removeAttribute('maze-controls');
                rig.dataset.aerial = 'true';
            }} else {{
                marker.setAttribute('visible', false);
                var p = JSON.parse(rig.dataset.savedPos);
                var cr = JSON.parse(rig.dataset.savedCamRot);
                rig.setAttribute('position', p);
                rig.setAttribute('rotation', '0 180 0');
                cam.setAttribute('rotation', cr);
                cam.setAttribute('look-controls', 'enabled', true);
                rig.setAttribute('maze-controls', '');
                rig.dataset.aerial = 'false';
            }}
            }});
            </script>
            """
             '</head>',
             '<body>',
             '<a-scene>',
             # Decoration:
             '<a-light type="ambient" color="#223" intensity="10"></a-light>',
             '<a-light type="directional" color="#446" position="150 200 100" intensity="15"></a-light>',
             '<a-assets>',
                f'<img id="floor-tex" src="data:image/jpeg;base64,{floor_b64}">',
                f'<img id="wall-tex" src="data:image/jpeg;base64,{wall_b64}">',
                f'<img id="sky-tex"  src="data:image/jpeg;base64,{sky_b64}">',
                f'<img id="moon-tex" src="data:image/jpeg;base64,{moon_b64}">',
             '</a-assets>',
             f'<a-sphere id="moon" radius="10" src="#moon-tex" visible="visible" position="150 200 0"></a-sphere>',
             # Camera
             f'<a-entity id="rig" maze-controls position="{1 * scale} 1.25 {1 * scale}" rotation="0 180 0">',
             f' <a-camera wasd-controls="enabled: false" look-controls position="0 0 0"></a-camera>',
             f'</a-entity>',
             f'<a-sphere id="marker" radius="0.5" color="red" visible="false" position="{1 * scale} {scale + 0.5} -2.5"></a-sphere>',
            ]
    # Sky
    lines.append('<a-sky src="#sky-tex"></a-sky>')

    # Floor:
    floor_x = (maze.shape[1] - 1) * scale / 2
    floor_z = (maze.shape[0] - 1) * scale / 2
    floor_w = maze.shape[1] * scale
    floor_d = maze.shape[0] * scale
    lines.append(
        f'<a-plane position="{floor_x} 0 {floor_z}" rotation="-90 0 0" '
        f'width="{floor_w}" height="{floor_d}" material="src: #floor-tex; repeat: {floor_w//scale} {floor_d//scale}"></a-plane>'
        )
    lines.append(f'<a-box position="2 1 0" width="{scale}" height="{scale}"'
                             f' depth="{scale}" src="#wall-tex" class="wall"> </a-box>'
                            )
    # Define the walls
    for row in range(maze.shape[0]):
        for col in range(maze.shape[1]):
            if maze[row][col]: # If True
                x = col * scale
                y = scale / 2
                z = row * scale
                lines.append(f'<a-box position="{x} {y} {z}" width="{scale}" height="{scale}"'
                             f' depth="{scale}" src="#wall-tex" class="wall"> </a-box>'
                            )
    # End of the file
    lines += [
        '</a-scene>',
        '</body>',
        '</html>'
    ]
    
    # Write the file
    with open(path, 'w') as f:
        f.write('\n'.join(lines))

    return path