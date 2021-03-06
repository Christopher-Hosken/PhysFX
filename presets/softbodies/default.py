import bpy
obj = bpy.context.object
scene = bpy.context.scene
softbody = obj.modifiers["Softbody"]

softbody.settings.friction = 0.5
softbody.settings.mass = 1.0
softbody.settings.use_goal = True
softbody.settings.goal_spring = 0.5
softbody.settings.goal_friction = 0.0
softbody.settings.goal_default = 0.699999988079071
softbody.settings.goal_min = 0.0
softbody.settings.goal_max = 1.0
softbody.settings.use_edges = True
softbody.settings.pull = 0.5
softbody.settings.push = 0.5
softbody.settings.damping = 0.5
softbody.settings.plastic = 0
softbody.settings.bend = 0.0
softbody.settings.spring_length = 0
softbody.settings.use_edge_collision = False
softbody.settings.use_face_collision = False
softbody.settings.aerodynamics_type = 'SIMPLE'
softbody.settings.aero = 0
softbody.settings.use_stiff_quads = False
softbody.settings.shear = 1.0
softbody.settings.use_self_collision = False
softbody.settings.collision_type = 'AVERAGE'
softbody.settings.ball_size = 0.49000000953674316
softbody.settings.ball_stiff = 1.0
softbody.settings.ball_damp = 0.5