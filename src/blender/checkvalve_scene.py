"""Original controllable Blender cutaway. Run with Blender --background --python."""
import argparse
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
args = argparse.ArgumentParser()
args.add_argument('--preview', action='store_true')
args.add_argument('--render', action='store_true')
args.add_argument('--draft', action='store_true')
args.add_argument('--timing', type=Path)
args.add_argument('--start-frame', type=int, default=1)
args.add_argument('--out', type=Path, default=ROOT/'outputs/blender')
options = args.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
options.out.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 50 if options.preview or options.draft else 100
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 1200
scene.world.color = (0.025, 0.035, 0.055)
scene.view_settings.view_transform = 'Standard'
scene.render.image_settings.file_format = 'PNG'

def material(name, color, metallic=0.0, roughness=0.35, emission=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*color, 1)
    shader.inputs['Metallic'].default_value = metallic
    shader.inputs['Roughness'].default_value = roughness
    shader.inputs['Emission Color'].default_value = (*color, 1)
    shader.inputs['Emission Strength'].default_value = emission
    return mat

housing_mat = material('Slate blue housing', (0.16,0.28,0.39), 0.5)
seat_mat = material('Silver fixed seat', (0.55,0.68,0.77), 0.65)
poppet_mat = material('Ivory solid poppet', (0.85,0.89,0.86), 0.45)
spring_mat = material('Gold spring', (0.93,0.59,0.14), 0.65)
water_mat = material('Cyan water tracer', (0.03,0.72,0.68), 0.05, emission=0.45)
back_mat = material('Navy studio', (0.018,0.037,0.065), roughness=0.8)
back_nodes=back_mat.node_tree.nodes
back_nodes.clear()
back_output=back_nodes.new('ShaderNodeOutputMaterial')
back_emission=back_nodes.new('ShaderNodeEmission')
back_emission.inputs['Color'].default_value=(0.008,0.018,0.036,1)
back_emission.inputs['Strength'].default_value=0.6
back_mat.node_tree.links.new(back_emission.outputs[0],back_output.inputs['Surface'])

def smooth_object(obj, mat):
    obj.data.materials.append(mat)
    if hasattr(obj.data, 'polygons'):
        for polygon in obj.data.polygons:
            polygon.use_smooth = True
    return obj

def cylinder(name, x, radius, length, mat):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=radius, depth=length, location=(x,0,0), rotation=(0,math.pi/2,0))
    obj = bpy.context.object
    obj.name = name
    bevel = obj.modifiers.new('Small edge bevel', 'BEVEL')
    bevel.width = 0.035
    bevel.segments = 2
    return smooth_object(obj, mat)

def tube(name, x1, x2, outer, inner, mat, cutaway=False):
    # Rear semicircle only for the chamber: exposes all internal components.
    count = 48
    angles = [math.pi*i/count for i in range(count+1)] if cutaway else [2*math.pi*i/count for i in range(count+1)]
    vertices = [(x, r*math.sin(a), r*math.cos(a)) for x,r in [(x1,outer),(x2,outer),(x1,inner),(x2,inner)] for a in angles]
    n = len(angles)
    faces = []
    for i in range(n-1):
        faces.extend([(i,i+1,n+i+1,n+i), (2*n+i,3*n+i,3*n+i+1,2*n+i+1), (i,2*n+i,2*n+i+1,i+1), (n+i,n+i+1,3*n+i+1,3*n+i)])
    if cutaway:
        faces.extend([(0,n,3*n,2*n),(n-1,3*n-1,4*n-1,2*n-1)])
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(obj)
    return smooth_object(obj, mat)

tube('Rear cutaway chamber', -1.5,2.15,1.07,0.96,housing_mat,True)
tube('Inlet pipe cutaway', -4,-1.5,0.64,0.51,housing_mat,True)
tube('Outlet pipe cutaway', 2.15,4,0.64,0.51,housing_mat,True)
tube('Fixed annular seat', -.99,-.89,.96,.49,seat_mat)
tube('Fixed spring retainer perimeter', 1.62,1.75,.96,.91,seat_mat)
tube('Fixed spring retainer cup',1.62,1.75,.38,.08,seat_mat)
for i,angle in enumerate([0,2*math.pi/3,4*math.pi/3]):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.69,.64*math.cos(angle),.64*math.sin(angle)))
    spoke=bpy.context.object
    spoke.name=f'Fixed retainer spoke {i}'
    spoke.rotation_euler.x=angle
    spoke.scale=(.13,.56,.055)
    smooth_object(spoke,seat_mat)
poppet = cylinder('Moving solid poppet', -.81,.62,.16,poppet_mat)
stem = cylinder('Moving axial stem', .4,.055,2.2,seat_mat)
curve = bpy.data.curves.new('Compressible coil geometry', 'CURVE')
curve.dimensions = '3D'
curve.bevel_depth = .038
curve.bevel_resolution = 3
spline = curve.splines.new('POLY')
steps = 240
spline.points.add(steps)
spring = bpy.data.objects.new('Animated spring',curve)
scene.collection.objects.link(spring)
curve.materials.append(spring_mat)
tracers = []
for i in range(16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=.055)
    obj = bpy.context.object
    obj.name = f'Flow tracer {i:02d}'
    smooth_object(obj,water_mat)
    tracers.append(obj)

def smooth(value):
    value = max(0,min(1,value))
    return value*value*(3-2*value)

TIMING=json.loads(options.timing.read_text(encoding='utf-8')) if options.timing else {'open_start':16,'close_start':25,'condition_start':34.5,'recap_start':39}
def opening(t):
    if t < TIMING['open_start']: return 0.0
    if t < TIMING['close_start']: return smooth((t-TIMING['open_start'])/2.2)
    if t < TIMING['condition_start']: return 1-smooth((t-TIMING['close_start'])/2)
    if t < TIMING['recap_start']: return smooth((t-TIMING['condition_start']-1.2)/1.8)
    phase = ((t-TIMING['recap_start'])%5)/5
    return smooth(phase/.25) if phase<.5 else 1-smooth((phase-.5)/.25)

def point_on_path(points, u):
    distances = [(b-a).length for a,b in zip(points,points[1:])]
    target = (u%1)*sum(distances)
    for a,b,distance in zip(points,points[1:],distances):
        if target <= distance: return a.lerp(b,target/distance)
        target -= distance
    return points[-1]

def update_geometry(frame_number, update_spring=True):
    t = (frame_number-1)/24
    amount = opening(t)
    x = -.81+.70*amount
    poppet.location.x = x
    stem.location.x = x+1.21
    start, end = x+.12,1.64
    if update_spring:
        for i,p in enumerate(spline.points):
            u = i/steps
            angle = u*math.pi*12
            p.co = (start+(end-start)*u,.28*math.cos(angle),.28*math.sin(angle),1)
    forward = (TIMING['open_start']<=t<TIMING['close_start']) or (TIMING['condition_start']<=t<TIMING['recap_start']) or (t>=TIMING['recap_start'] and ((t-TIMING['recap_start'])%5)<2.5)
    reverse = (t<8) or (TIMING['close_start']+2<=t<TIMING['condition_start']) or (t>=TIMING['recap_start'] and ((t-TIMING['recap_start'])%5)>3.75)
    if forward and amount>.3:
        gap_x = (-.89+(x-.08))/2
        # Pass through the annular seat bore, then around the solid poppet.
        coords = [(-3.9,-.25,.18),(-1.1,-.25,.18),(gap_x,-.35,.2),(gap_x,-.38,.75),(x+.35,-.38,.78),(1.4,-.35,.78),(1.86,-.30,.65),(2.35,-.25,.18),(3.9,-.25,.18)]
    elif reverse:
        coords = [(3.9,-.25,.18),(2.4,-.25,.18),(1.85,-.30,.76),(x+.3,-.38,.78),(x+.20,-.38,.50)]
    else:
        coords = [(-3.9,-.25,.18),(-1.10,-.25,.18)]
    points = [Vector(c) for c in coords]
    for i,obj in enumerate(tracers):
        obj.hide_render = not (forward or reverse)
        obj.location = point_on_path(points,t*.22+i/len(tracers))

# Bake transforms and coil shape keys so the saved .blend also works without handlers.
update_geometry(1)
basis = spring.shape_key_add(name='Closed spring')
opened = spring.shape_key_add(name='Compressed spring')
for i,p in enumerate(opened.data):
    u = i/steps
    p.co.x = -.81+.70+.12+(1.64-(-.81+.70+.12))*u
for frame in range(1,1201):
    update_geometry(frame,update_spring=False)
    opened.value = opening((frame-1)/24)
    opened.keyframe_insert(data_path='value',frame=frame)
    poppet.keyframe_insert(data_path='location',frame=frame)
    stem.keyframe_insert(data_path='location',frame=frame)
    for obj in tracers:
        obj.keyframe_insert(data_path='location',frame=frame)
        obj.keyframe_insert(data_path='hide_render',frame=frame)
# Handler updated curve control points while baking; restore closed basis geometry.
for i,p in enumerate(spline.points):
    p.co = (*basis.data[i].co,1)

bpy.ops.mesh.primitive_plane_add(size=200, location=(0,4,0), rotation=(math.pi/2,0,0))
smooth_object(bpy.context.object,back_mat)
bpy.context.object.name='Navy backdrop'
for name,location,power,size in [('Key',(-3,-5,6),700,5),('Fill',(4,-4,2),450,4),('Rim',(0,3,5),650,4)]:
    light_data = bpy.data.lights.new(name,'AREA')
    light_data.energy=power
    light_data.shape='DISK'
    light_data.size=size
    obj=bpy.data.objects.new(name,light_data)
    scene.collection.objects.link(obj)
    obj.location=location
    obj.rotation_euler=(Vector((0,0,0))-obj.location).to_track_quat('-Z','Y').to_euler()
camera_data=bpy.data.cameras.new('Explainer camera')
camera=bpy.data.objects.new('Explainer camera',camera_data)
scene.collection.objects.link(camera)
camera.location=(1.3,-16,5)
camera.rotation_euler=(Vector((0,0,0))-camera.location).to_track_quat('-Z','Y').to_euler()
camera_data.type='ORTHO'
camera_data.ortho_scale=17
scene.camera=camera
scene.frame_set(1)
blend_path=options.out/'checkvalve.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
if options.preview:
    for label,frame in [('closed',289),('open',505),('closing',637),('recap',1081)]:
        scene.frame_set(frame)
        scene.render.filepath=str(options.out/f'{label}.png')
        bpy.ops.render.render(write_still=True)
if options.render:
    frames_dir=ROOT/'work/hybrid/frames'
    frames_dir.mkdir(parents=True,exist_ok=True)
    scene.frame_start=options.start_frame
    scene.render.filepath=str(frames_dir/'frame_')
    bpy.ops.render.render(animation=True)
print(json.dumps({'blend':str(blend_path),'frames':1200,'fps':24,'duration':50,'timing_status':'measured Piljae timing supplied' if options.timing else 'provisional; retime from final Piljae audio','preview':options.preview}))
