import maya.cmds as cmds
from functools import partial

# INTERFACE

window_name = "rig_tool"
window_title = "Simple Rig by RooWiki"
window_w = 200
window_h = 168

def create_window():
    if cmds.window(window_name, query=True, exists=True):
        cmds.deleteUI(window_name)
    cmds.window(window_name)
    cmds.window(window_name, edit=True, w=window_w+2, h=window_h, title=window_title, mnb=False, mxb=False,  s=False)
   
    cmds.columnLayout("main_colum", w=window_w, h=window_h)
    create_customUI()
   
    cmds.showWindow(window_name)
   
def create_customUI():
    cmds.button("rig_button", label="Rig", w = window_w, h=40, command=rigg)
   
    cmds.frameLayout("cuntrol_scale_frame", label="Control Scale", w=window_w, parent="main_colum", cl=True, bgc=(.255,.0,.255))
    cmds.rowLayout("control_scale_row", nc=3, w=window_w)
   
    cmds.floatField("scale_floatField", precision=2, w=window_w/3, value=0.2)
    cmds.button("samll_burron", label="Small", w=window_w/3, command=partial(scale_control, "small"))
    cmds.button("big_button", label="Big", w=window_w/3, command=partial(scale_control, "big"))
   
    cmds.frameLayout("control_color_frame", label="Control Color", w=window_w, parent="main_colum", cl=True, bgc=(0.255,0.0,0.255))
    cmds.colorIndexSliderGrp("color_index_slider", max=31, v=50, changeCommand=color_control)
    cmds.button("set_color", label="Set Color", h=30, command=color_control)
   
   
# FUNCTIONS

  
def color_control(*args):
    color_index = cmds.colorIndexSliderGrp("color_index_slider", query=True, value=True)
    selection = cmds.ls(selection=True)
    
    for control in selection:
        shape = cmds.listRelatives(control, children=True)[0] 
        cmds.setAttr(shape+".overrideEnabled",1)
        cmds.setAttr(shape+".overrideColor",color_index-1)

def scale_control(mode, *args):
    scale_factor = cmds.floatField("scale_floatField", query=True, value=True)
    selection = cmds.ls(selection=True)
    
    for control in selection:
        if mode == "small": 
            cmds.scale(1.0-scale_factor, 1.0-scale_factor, 1.0-scale_factor, control+".cv[0:]")
        else:
            cmds.scale(1.0+scale_factor, 1.0+scale_factor, 1.0+scale_factor, control+".cv[0:]")

  
def rigg(*args):

    selection = cmds.ls(selection = True)
    if len(selection)==0:
        cmds.warning("No has seleccionado ningun objeto, selecciona un objeto")
    elif len(selection)>2:
        cmds.warning("Por favor selecciona un joint o un joint y una curva")
    else:
        if len(selection) == 1:
            if cmds.objectType(selection[0])!="joint":
                cmds.warning("Por favor selecione un joint")
                return
               
        if len(selection) == 2:
            shape = cmds.listRelatives(selection[1],children=True)[0]
            if cmds.objectType(selection[0])=="joint" and cmds.objectType(shape)=="nurbsCurve":
                pass
            else:
                cmds.warning("Por favor selecione un joint y luego una curva")
                return
               
        selected_joint = selection[0]
        cmds.select(selected_joint,hi=True)
        all_joint = cmds.ls(selection=True)
       
        control_list = []
        grp_list = []
        control_scale = 1
           
        for n in range(len(all_joint)-1):
           
            if len(selection) == 1:
                newcontrol = cmds.circle(name=all_joint[n]+"_ctrl",radius = control_scale)[0]
                control_list.append(newcontrol)
                cmds.rotate(0,90,0, newcontrol)
                cmds.scale(3,3,3, newcontrol)
            if len(selection) == 2:
                newcontrol = cmds.duplicate(selection[1])[0]
                control_list.append(newcontrol)
               
            cmds.makeIdentity(apply=True)
            cmds.DeleteHistory()
           
            grp = cmds.group(name = newcontrol + "_grp", empty=True)
            grp_list.append(grp)
            cmds.parent(newcontrol, grp)
           
            joint_position = cmds.xform(all_joint[n], query=True, translation=True, worldSpace=True)
            cmds.xform(grp, translation=joint_position)
            orient_cons = cmds.orientConstraint(all_joint[n], grp)
            cmds.delete(orient_cons)
           
            cmds.parentConstraint(newcontrol,all_joint[n])
           
        for j in range(len(all_joint)-2):
            cmds.parent(grp_list[j+1], control_list[j])
        cmds.select(control_list)
   
   
   
create_window()