import bpy
import addon_utils
from bpy.types import Panel
from bl_ui.utils import PresetPanel

class PhysFXToolsPro_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "PhysFX Tools Pro"

class PhysFXToolsPro_PT_BasePanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "PhysFXTools-Pro"
    bl_idname = "PANEL_PT_physfxtoolspro"

    def draw(self, context):
        pass

class PhysFXToolsPro_PT_GluePanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "Glue"
    bl_idname = "PANEL_PT_physfxtoolspro_glue"
    bl_parent_id = "PANEL_PT_physfxtoolspro"

    def draw(self, context):
        props = context.scene.physfxtoolspro_props
        layout = self.layout

        row = layout.row()
        row.prop(props, "glue_collection", text="Use Collection")

        row = layout.row()
        row.prop(props, "breaking_threshold", text="Strength")
        
        row = layout.row()
        row.prop(props, "glue_distance", text="Distance")

        row = layout.row()
        row.operator("physfxtoolspro.gluebodies", text="Glue", icon="MOD_NOISE")
        row.operator("physfxtoolspro.deleteglue", text="", icon='X')

class PhysFXToolsPro_PT_ProxyMeshPanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "Proxy Mesh"
    bl_idname = "PANEL_PT_physfxtoolspro_proxymesh"
    bl_parent_id = "PANEL_PT_physfxtoolspro"

    def draw(self, context):
        props = context.scene.physfxtoolspro_props
        layout = self.layout

        row = layout.row()
        row.prop(props, "proxy_resolution", text="Resolution")

        row = layout.row()
        row.prop(props, "proxy_offset", text="Offset")

        row = layout.row()
        row.operator("physfxtoolspro.makeproxymesh", text="Create Proxy", icon='MOD_MESHDEFORM')
        row.operator("physfxtoolspro.deleteproxymesh", text="", icon="X")

class PhysFXToolsPro_PT_GroupingBasePanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "Grouping"
    bl_idname = "PANEL_PT_physfxtoolspro_groupingbase"
    bl_parent_id = "PANEL_PT_physfxtoolspro"

    def draw(self, context):
        pass

class PhysFXToolsPro_PT_GroupCollisionsPanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "Collisions"
    bl_idname = "PANEL_PT_physfxtoolspro_groupcollisions"
    bl_parent_id = "PANEL_PT_physfxtoolspro_groupingbase"

    def draw(self, context):
        props = context.scene.physfxtoolspro_props
        layout = self.layout

        row = layout.row()
        col = row.column()
        col.label(text = "Particles")
        col.prop(props, "particle_friction", text="Friction")
        col.prop(props, "particle_damping", text="Damping")
        col.prop(props, "particle_random", text="Random")
        col.prop(props, "kill_particles", text="Kill Particles")

        row = layout.row()
        col = row.column()
        col.label(text = "Cloth")
        col.prop(props, "cloth_friction", text="Friction")
        col.prop(props, "cloth_damping", text="Damping")
        col.prop(props, "cloth_thickness", text="Thickness")

        row = layout.row()
        row.operator("physfxtoolspro.groupcollisions", text="Group Collisions")
        row.operator("physfxtoolspro.deletecollisions", text="", icon="X")

class PhysFXToolsPro_PT_GroupRigidBodiesPanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "Rigid Bodies"
    bl_idname = "PANEL_PT_physfxtoolspro_grouprigidbodies"
    bl_parent_id = "PANEL_PT_physfxtoolspro_groupingbase"

    def draw(self, context):
        props = context.scene.physfxtoolspro_props
        layout = self.layout

        row = layout.row()
        col = row.column()
        col.label(text="Settings")
        col.prop(props, 'rigidbody_shape', text="Shape")
        col.prop(props, 'rigidbody_source', text="Source")
        col.prop(props, 'rigidbody_is_active', text="Active")
        if props.rigidbody_is_active:
            col.prop(props, 'rigidbody_mass', text="Mass")
        col.prop(props, 'rigidbody_friction', text="Friction")
        col.prop(props, 'rigidbody_bounce', text="Bounciness")
        col.prop(props, 'rigidbody_margin', text="Margin")

        row = layout.row()
        row.operator("physfxtoolspro.grouprigidbodies", text="Group Rigid Bodies")
        row.operator("physfxtoolspro.deleterigidbodies", text="", icon="X")

class PHYSFXTOOLSPRO_PT_SoftbodyPresets(PresetPanel, Panel):
    bl_label = "Softbody Presets"
    preset_subdir = 'physfxtoolspro/softbodies'
    preset_operator = 'script.execute_preset'
    preset_add_operator = 'physfxtoolspro.addsoftbodypreset'

class PhysFXToolsPro_PT_SoftbodyPanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "Soft Body Presets"
    bl_idname = "PANEL_PT_physfxtoolspro_deform"
    bl_parent_id = "PANEL_PT_physfxtoolspro"

    def draw(self, context):
        obj = context.active_object
        softbody_active = False
        if obj is not None:
            for mod in obj.modifiers:
                if mod.type == "SOFT_BODY":
                    softbody_active = True

        scene = context.scene
        layout = self.layout

        row = layout.row()
        row.operator("physfxtoolspro.addsoftbody", text="Add Softbody")
        row.operator("physfxtoolspro.deletesoftbody", text="", icon="X")

        row = layout.row()
        row.label(text="Presets: ")
        PHYSFXTOOLSPRO_PT_SoftbodyPresets.draw_panel_header(row)
        row.enabled = (softbody_active)

class PhysFXToolsPro_PT_CellFracturePanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "Cell Fracture"
    bl_idname = "PANEL_PT_physfxtoolspro_cellfracture"
    bl_parent_id = "PANEL_PT_physfxtoolspro"

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        row = layout.row()

        if addon_utils.check("object_fracture_cell")[0]:
            row.operator("object.add_fracture_cell_objects", text="Cell Fracture")
            row.operator("physfxtoolspro.importcellfracturepresets", text="", icon="ADD")
        else:
            row.label(text="Please enable the Cell Fracture addon!")

class PhysFXToolsPro_PT_ExtraPanel(PhysFXToolsPro_PT_Panel, Panel):
    bl_label = "Extra"
    bl_idname = "PANEL_PT_physfxtoolspro_extra"
    bl_parent_id = "PANEL_PT_physfxtoolspro"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Get in contact!")
        row = layout.row()
        row.label(text="hoskenchristopher@gmail.com")
        row = layout.row()
        row.operator('wm.url_open', text='Discord').url = "https://discordapp.com/channels/@me/Cjhosken#7147/"
        row.operator('wm.url_open', text='Instagram').url = "https://www.instagram.com/cjhosken/"
        row = layout.row()
        row.operator('wm.url_open', text='Artstation').url = "https://www.artstation.com/christopherhosken"
        row.operator('wm.url_open', text='Report Bug').url = "https://github.com/Christopher-Hosken/PhysFX-Tools/issues"