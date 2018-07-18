
import os
import pymel.core as pm


def select(vrsceneList):
    new_vrsceneList = []

    start = pm.getAttr("defaultRenderGlobals.startFrame")
    end = pm.getAttr("defaultRenderGlobals.endFrame")

    if not pm.about(batch=True):
        vrsettings = pm.PyNode("vraySettings")
        anim_type = vrsettings.animType.get()
        if anim_type <= 1 and vrsettings.animBatchOnly.get():
            start = end = int(pm.currentTime())

    # roughly adding 2 frames, in case motion blur is on
    start = start - 2
    end = end + 2

    vrsType = ['bitmaps', 'geometry', 'materials', 'nodes', 'textures']

    for vrscene in vrsceneList:
        vrsceneDir = os.path.dirname(vrscene)
        all_vrsfiles = os.listdir(vrsceneDir)

        if len(all_vrsfiles) == (len(vrsType) + 1):
            # old style (not each frame)
            new_vrsceneList.append(vrscene)
            continue

        selected_vrscenes = []
        for vrs in all_vrsfiles:
            if not vrs.endswith(".vrscene"):
                continue
            if any(vrs.endswith("_{}.vrscene".format(typ)) for typ in vrsType):
                continue

            frame_num = int(vrs.split(".")[0].split("_")[-1])
            if frame_num >= start and frame_num <= end:
                selected_vrscenes.append(os.path.join(vrsceneDir, vrs))

        new_vrsceneList.append(selected_vrscenes)

    return new_vrsceneList
