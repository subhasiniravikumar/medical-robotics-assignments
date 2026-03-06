import time, math
import browserbotics as bb

# ================================================================
#  HOSPITAL PROCEDURE ROOM (DUAL SETUP + WHEELED MOVER)
#  Robot 1 (X=0.0) | Robot 2 (X=6.5) | Mover Robot (Y=1.95)
#  Smart Transport Logic + High-Walled Premium OT Design
# ================================================================

bb.setGravity(0, 0, 0)
bb.addGroundPlane()

# ── Robust Pose Helper ──────────────────────────────────────────
def set_pose(body, pos, quat):
    if hasattr(bb, 'resetBasePositionAndOrientation'):
        bb.resetBasePositionAndOrientation(body, pos, quat)
    elif hasattr(bb, 'resetBasePose'):
        bb.resetBasePose(body, pos, quat)
    elif hasattr(bb, 'setBasePose'):
        bb.setBasePose(body, pos, quat)
    elif hasattr(bb, 'resetBodyPose'):
        bb.resetBodyPose(body, pos, quat)
    else:
        pass 

# ================================================================
#  PANDA ROBOT ARMS
# ================================================================
OFFSET_X = 6.5  

# Robot 1 (Bed 1)
robot1 = bb.loadURDF('panda.urdf', fixedBase=True, globalScaling=1.35)
# Robot 2 (Bed 2)
robot2 = bb.loadURDF('panda.urdf', fixedBase=True, globalScaling=1.35)
set_pose(robot2, [OFFSET_X, 0.0, 0.0], [0, 0, 0, 1])

# Robot 3 (Mobile Mover on AGV Cart)
MOVER_Y = 1.95
robot3 = bb.loadURDF('panda.urdf', fixedBase=True, globalScaling=1.10)

# Redesigned Mobile Cart (Base, Accent, and 4 Wheels)
mover_base = bb.createBody('box', halfExtent=[0.25, 0.35, 0.15], position=[0.6, MOVER_Y, 0.15], color='#D0D0D0', mass=0)
mover_accent = bb.createBody('box', halfExtent=[0.26, 0.36, 0.02], position=[0.6, MOVER_Y, 0.20], color='#00AAFF', mass=0)

mover_w1 = bb.createBody('sphere', radius=0.08, position=[0.6-0.2, MOVER_Y-0.25, 0.08], color='#222222', mass=0)
mover_w2 = bb.createBody('sphere', radius=0.08, position=[0.6+0.2, MOVER_Y-0.25, 0.08], color='#222222', mass=0)
mover_w3 = bb.createBody('sphere', radius=0.08, position=[0.6-0.2, MOVER_Y+0.25, 0.08], color='#222222', mass=0)
mover_w4 = bb.createBody('sphere', radius=0.08, position=[0.6+0.2, MOVER_Y+0.25, 0.08], color='#222222', mass=0)

ee_link = 10
home_arm_jpos = [0, -0.5, 0., -1.5, 0.1, 1, 0]
for i, jp in enumerate(home_arm_jpos):
    bb.setJointMotorControl(robot1, i, targetPosition=jp)
    bb.setJointMotorControl(robot2, i, targetPosition=jp)

# ================================================================
#  UI CONTROLS 
# ================================================================
# Robot 1
bb.addDebugButton('[R1] Left')
bb.addDebugButton('[R1] Right')
bb.addDebugButton('[R1] Forward')
bb.addDebugButton('[R1] Backward')
bb.addDebugButton('[R1] Up')
bb.addDebugButton('[R1] Down')
bb.addDebugButton('[R1] Grab Tool')
bb.addDebugButton('[R1] Drop Tool')

# Robot 2
bb.addDebugButton('[R2] Left')
bb.addDebugButton('[R2] Right')
bb.addDebugButton('[R2] Forward')
bb.addDebugButton('[R2] Backward')
bb.addDebugButton('[R2] Up')
bb.addDebugButton('[R2] Down')
bb.addDebugButton('[R2] Grab Tool')
bb.addDebugButton('[R2] Drop Tool')

# Shared Rotation
bb.addDebugSlider('rx', math.pi,   -math.pi, math.pi)
bb.addDebugSlider('ry', 0,         -math.pi, math.pi)
bb.addDebugSlider('rz', 0,         -math.pi, math.pi)
bb.addDebugToggle('use rotation')

# MOVER ROBOT CONTROLS
bb.addDebugButton('[Mover] Forward (To R2)')
bb.addDebugButton('[Mover] Backward (To R1)')
bb.addDebugButton('[Mover] Pick from Tray')
bb.addDebugButton('[Mover] Drop to Tray')

# ================================================================
#  ROOM (3 Side Walls, Taller, OT Colors, No Ceiling/Entrance)
# ================================================================
# Clinical Color Palette
FL       = '#E8EBEA'       # Light clinical gray floor
FRONT_WALL = '#B2E2E6'     # Surgical light blue
SIDE_WALL  = '#A8D5BA'     # Surgical pale green
TRIM_COL   = '#5A6A7A'     # Baseboards
L_BULB     = '#FFFFEE'     # Warm bright light
L_FIXTURE  = '#F0F0F0'     # White fixture

BDF  = '#D0CCCA'; MAT  = '#F8F6F2'; SHT  = '#F0F0EC'
BLK  = '#45B0A0'; BLD  = '#339988'; SKN  = '#C49060'; SKD  = '#A87040'
MOB  = '#1A1818'; SUS  = '#182818'; SGN  = '#00DD44'; POL  = '#B8BCC0'
ORG  = '#E87800'; RED  = '#CC2222'; GRY  = '#888890'; YEL  = '#E8C800'
DKG  = '#383838'; GRN_S = '#005522'

def b(x, y, z): return [x, y, z]

RW = 15.0; RD = 8.0; WH = 4.5  # Increased Height and Depth
CEN_X = OFFSET_X / 2.0  

# Floor
bb.createBody('box', halfExtent=[RW/2, RD/2, 0.015], position=b(CEN_X, 0.0, -0.228), color=FL, mass=0)

# FRONT WALL (Y = 4.0)
bb.createBody('box', halfExtent=[RW/2, 0.1, WH/2], position=b(CEN_X, 4.0, WH/2 - 0.24), color=FRONT_WALL, mass=0)
bb.createBody('box', halfExtent=[RW/2, 0.11, 0.08], position=b(CEN_X, 3.99, -0.15), color=TRIM_COL, mass=0)

# LEFT WALL
bb.createBody('box', halfExtent=[0.1, RD/2, WH/2], position=b(CEN_X - RW/2, 0.0, WH/2 - 0.24), color=SIDE_WALL, mass=0)
bb.createBody('box', halfExtent=[0.11, RD/2, 0.08], position=b(CEN_X - RW/2 + 0.01, 0.0, -0.15), color=TRIM_COL, mass=0)

# RIGHT WALL
bb.createBody('box', halfExtent=[0.1, RD/2, WH/2], position=b(CEN_X + RW/2, 0.0, WH/2 - 0.24), color=SIDE_WALL, mass=0)
bb.createBody('box', halfExtent=[0.11, RD/2, 0.08], position=b(CEN_X + RW/2 - 0.01, 0.0, -0.15), color=TRIM_COL, mass=0)

# ── WALL LIGHTS ──
# Front Wall Lights
for lx in [-2.0, 1.5, 5.0, 8.5]:
    bb.createBody('box', halfExtent=[0.4, 0.05, 0.1], position=b(lx, 3.9, 3.8), color=L_FIXTURE, mass=0)
    bb.createBody('box', halfExtent=[0.38, 0.06, 0.08], position=b(lx, 3.88, 3.8), color=L_BULB, mass=0) 

# Side Wall Lights
for ly in [-2.5, 0.5, 3.0]:
    # Left Wall
    bb.createBody('box', halfExtent=[0.05, 0.4, 0.1], position=b(-4.15, ly, 3.8), color=L_FIXTURE, mass=0)
    bb.createBody('box', halfExtent=[0.06, 0.38, 0.08], position=b(-4.13, ly, 3.8), color=L_BULB, mass=0)
    # Right Wall
    bb.createBody('box', halfExtent=[0.05, 0.4, 0.1], position=b(10.65, ly, 3.8), color=L_FIXTURE, mass=0)
    bb.createBody('box', halfExtent=[0.06, 0.38, 0.08], position=b(10.63, ly, 3.8), color=L_BULB, mass=0)

# ── CORNER FLOWER POTS ──
corners = [(-3.8, 3.5), (10.3, 3.5), (-3.8, -3.5), (10.3, -3.5)]
for cx, cy in corners:
    # Modern white planter base
    bb.createBody('box', halfExtent=[0.25, 0.25, 0.3], position=b(cx, cy, 0.07), color='#F5F5F5', mass=0)
    # Lush green plants (composed of spheres)
    bb.createBody('sphere', radius=0.35, position=b(cx, cy, 0.5), color='#2E8B57', mass=0)
    bb.createBody('sphere', radius=0.25, position=b(cx+0.1, cy, 0.7), color='#228B22', mass=0)
    bb.createBody('sphere', radius=0.25, position=b(cx-0.1, cy+0.1, 0.65), color='#32CD32', mass=0)


# ================================================================
#  MODULAR SETUP BUILDER
# ================================================================
setup_data = []

T_HALF = 0.52   
H_RAD  = 0.13   
DOC_Z = 0.0
TORSO_Z = DOC_Z + T_HALF - 0.24
HEAD_Z  = DOC_Z + 2*T_HALF + H_RAD - 0.24

def build_ot_setup(ox):
    # Pedestal
    bb.createBody('box', halfExtent=[0.20, 0.20, 0.02], position=[ox, 0, -0.02], color='#D8D6D0', mass=0)
    bb.createBody('box', halfExtent=[0.18, 0.18, 0.12], position=[ox, 0, -0.14], color='#E8E6E2', mass=0)
    bb.createBody('box', halfExtent=[0.25, 0.25, 0.04], position=[ox, 0, -0.20], color='#D0CEC8', mass=0)
    
    # Biohazard Bin
    BIN_X = ox - 1.2; BIN_Y = 0.0
    bb.createBody('box', halfExtent=[0.15, 0.15, 0.22], position=b(BIN_X, BIN_Y, 0.0), color=RED, mass=0)
    bb.createBody('box', halfExtent=[0.16, 0.16, 0.02], position=b(BIN_X, BIN_Y, 0.24), color=MOB, mass=0)
    
    # Anesthesia Machine
    AN_X = ox - 1.4; AN_Y = 1.3
    bb.createBody('box', halfExtent=[0.22, 0.22, 0.35], position=b(AN_X, AN_Y, 0.12), color='#E4E8EC', mass=0)
    bb.createBody('box', halfExtent=[0.18, 0.20, 0.25], position=b(AN_X, AN_Y, 0.72), color='#D0D4D8', mass=0)
    bb.createBody('box', halfExtent=[0.16, 0.02, 0.12], position=b(AN_X, AN_Y+0.21, 0.85), color=MOB, mass=0) 

    # IV Pole & Defibrillator (Mounted on Front Wall)
    IV_X = ox - 1.8; IV_Y = 1.50
    bb.createBody('box', halfExtent=[0.019,0.019,1.08], position=b(IV_X, IV_Y, 0.60 - 0.24), color=POL, mass=0)
    DF_X = ox - 1.5; DF_Y = 3.90; DF_Z = 1.10
    bb.createBody('box', halfExtent=[0.180,0.10,0.112], position=b(DF_X, DF_Y, DF_Z), color='#D4CEC4', mass=0)

    # Ultrasound Monitor
    UX = ox + 0.80; UY = 0.80
    bb.createBody('box', halfExtent=[0.022,0.022,0.90], position=b(UX, UY, 0.66), color=POL, mass=0)
    bb.createBody('box', halfExtent=[0.20,0.20,0.022], position=b(UX, UY, -0.218), color='#909898', mass=0)
    bb.createBody('box', halfExtent=[0.255,0.055,0.193], position=b(UX-0.34, UY, 1.46), color='#D8D4CC', mass=0)

    # Hospital Bed
    BX = ox - 0.90; BY = 0.55; BS = 0.60
    bb.createBody('box', halfExtent=[0.25, 0.4, 0.12], position=b(BX, BY, BS - 0.40), color='#505050', mass=0)
    bb.createBody('box', halfExtent=[0.46, 1.02, 0.04], position=b(BX, BY, BS - 0.15), color=BDF, mass=0)
    bb.createBody('box', halfExtent=[0.44, 0.98, 0.08], position=b(BX, BY, BS - 0.03), color=MAT, mass=0)
    for sx in [-0.46, 0.46]:
        bb.createBody('box', halfExtent=[0.02, 0.35, 0.12], position=b(BX+sx, BY+0.4, BS + 0.12), color='#E8EEF2', mass=0)

    # Patient
    PZ = BS + 0.05  
    bb.createBody('box', halfExtent=[0.30, 0.18, 0.04], position=b(BX, BY+0.80, PZ+0.04), color='#FAFAFA', mass=0)
    r_torso = bb.createBody('box', halfExtent=[0.24,0.31,0.072], position=b(BX, BY+0.29, PZ+0.072), color=SKN, mass=0)
    for px in [-0.28, 0.28]:
        bb.createBody('box', halfExtent=[0.04, 0.25, 0.05], position=b(BX+px, BY+0.25, PZ+0.05), color=SKN, mass=0)
    r_head = bb.createBody('sphere', radius=0.11, position=b(BX, BY+0.80, PZ+0.14), color=SKN, mass=0)
    bb.createBody('box', halfExtent=[0.45, 0.55, 0.08], position=b(BX, BY-0.30, PZ+0.08), color=BLK, mass=0)
    
    # Doctor & Console
    DOC_X = ox + 0.0; DOC_Y = -1.10
    r_doc_torso = bb.createBody('box', halfExtent=[0.20,0.17,T_HALF], position=b(DOC_X, DOC_Y, TORSO_Z), color=GRN_S, mass=0)
    r_doc_head  = bb.createBody('sphere', radius=H_RAD, position=b(DOC_X, DOC_Y, HEAD_Z), color=SKN, mass=0)
    r_doc_arm_l = bb.createBody('box', halfExtent=[0.22,0.05,0.05], position=b(DOC_X-0.18, DOC_Y-0.22, TORSO_Z+0.10), color=GRN_S, mass=0)
    r_doc_hand_l = bb.createBody('sphere', radius=0.055, position=b(DOC_X-0.36, DOC_Y-0.30, TORSO_Z+0.10), color=SKN, mass=0)
    r_doc_arm_r = bb.createBody('box', halfExtent=[0.22,0.05,0.05], position=b(DOC_X+0.18, DOC_Y-0.22, TORSO_Z+0.10), color=GRN_S, mass=0)
    r_doc_hand_r = bb.createBody('sphere', radius=0.055, position=b(DOC_X+0.36, DOC_Y-0.30, TORSO_Z+0.10), color=SKN, mass=0)

    CON_X = DOC_X; CON_Y = DOC_Y - 0.55
    bb.createBody('box', halfExtent=[0.50,0.35,0.48], position=b(CON_X, CON_Y, 0.24), color='#2A4858', mass=0)
    bb.createBody('box', halfExtent=[0.50,0.35,0.025], position=b(CON_X, CON_Y, 0.74), color='#1C3040', mass=0)

    # Surgical Trays
    TX = ox + 0.60; TY = 0.45; TZ = 0.52   
    bb.createBody('box', halfExtent=[0.23,0.16,0.012], position=b(TX, TY, TZ - 0.24), color='#C4C8CC', mass=0)
    r_tool   = bb.createBody('box', halfExtent=[0.022,0.088,0.015], position=b(TX, TY-0.04, TZ - 0.222), color=RED, mass=0)
    r_handle = bb.createBody('box', halfExtent=[0.020,0.035,0.014], position=b(TX, TY-0.13, TZ - 0.222), color=YEL, mass=0)

    setup_data.append({
        'r_torso': r_torso, 'r_head': r_head, 'bx': BX, 'by': BY, 'pz': PZ,
        'doc_x': DOC_X, 'doc_y': DOC_Y,
        'r_doc_torso': r_doc_torso, 'r_doc_head': r_doc_head,
        'r_doc_arm_l': r_doc_arm_l, 'r_doc_hand_l': r_doc_hand_l,
        'r_doc_arm_r': r_doc_arm_r, 'r_doc_hand_r': r_doc_hand_r,
        'r_tool': r_tool, 'r_handle': r_handle, 'tx': TX, 'ty': TY, 'tz': TZ
    })

build_ot_setup(0.0)       # Setup 1
build_ot_setup(OFFSET_X)  # Setup 2

# ================================================================
#  TRANSPORT OBJECTS (Box 1 on Tray 1, Box 2 on Tray 2)
# ================================================================
# Box 1 (Cyan) Starts at Setup 1's Tray
box1 = bb.createBody('box', halfExtent=[0.05, 0.05, 0.05], position=[0.60, 0.45, 0.56], color='#00FFFF', mass=0)
# Box 2 (Magenta) Starts at Setup 2's Tray
box2 = bb.createBody('box', halfExtent=[0.05, 0.05, 0.05], position=[7.10, 0.45, 0.56], color='#FF00FF', mass=0)

# Tracker variables: 1 = Tray 1, 2 = Tray 2, 3 = Carried by Mover
box1_loc = 1 
box2_loc = 2 
mover_carrying = 0  # 0 = none, 1 = Box 1, 2 = Box 2

# ================================================================
#  MAIN LOOP
# ================================================================
li = 0

btn_state = {
    'R1_L': 0, 'R1_R': 0, 'R1_F': 0, 'R1_B': 0, 'R1_U': 0, 'R1_D': 0, 'R1_G': 0, 'R1_Dr': 0,
    'R2_L': 0, 'R2_R': 0, 'R2_F': 0, 'R2_B': 0, 'R2_U': 0, 'R2_D': 0, 'R2_G': 0, 'R2_Dr': 0,
    'M_F': 0, 'M_B': 0, 'M_P': 0, 'M_D': 0
}

# R1 & R2 Variables
last_rx = math.pi; last_ry = 0; last_rz = 0; last_use_rot = 0
is_grab1 = False; is_grab2 = False

tool1_p1 = b(setup_data[0]['tx'], setup_data[0]['ty']-0.04, setup_data[0]['tz']-0.222)
tool1_p2 = b(setup_data[0]['tx'], setup_data[0]['ty']-0.13, setup_data[0]['tz']-0.222)
tool1_q  = [0, 0, 0, 1]

tool2_p1 = b(setup_data[1]['tx'], setup_data[1]['ty']-0.04, setup_data[1]['tz']-0.222)
tool2_p2 = b(setup_data[1]['tx'], setup_data[1]['ty']-0.13, setup_data[1]['tz']-0.222)
tool2_q  = [0, 0, 0, 1]

target1_x = 0.0; target1_y = 0.5; target1_z = 0.5
target2_x = OFFSET_X; target2_y = 0.5; target2_z = 0.5

# Mover Variables
mover_x = 0.6          # Starts aligned with Tray 1
mover_target_x = 0.6   # Destination X position

# Mover Animation Variables
mover_anim_state = 0  
mover_anim_timer = 0  

# Arm poses for the animation
mover_carry_jpos = [0, 0.5, 0, -1.5, 0, 2.0, 0] 
mover_reach_jpos = [0, 1.2, 0, -0.3, 0, 2.0, 0] 

while True:
    # --- ANTI-GLITCH FIX ---
    if li == 0:
        bb.stepSimulation(0.05)
        try:
            ep1, eq1 = bb.getLinkPose(robot1, ee_link)
            target1_x = ep1[0]; target1_y = ep1[1]; target1_z = ep1[2]
            ep2, eq2 = bb.getLinkPose(robot2, ee_link)
            target2_x = ep2[0]; target2_y = ep2[1]; target2_z = ep2[2]
        except Exception:
            pass

    t = li / 20.0

    # ── Visual Animations ──
    br = 0.008 * math.sin(t * 0.85)
    ctrl = math.sin(t * 0.6)
    ctrl2 = math.sin(t * 0.5 + 1.2)
    sway = 0.015 * math.sin(t * 0.25)

    for sd in setup_data:
        set_pose(sd['r_torso'], b(sd['bx'], sd['by']+0.29, sd['pz']+0.072+br), [0,0,0,1])
        set_pose(sd['r_head'],  b(sd['bx'], sd['by']+0.80, sd['pz']+0.14+br*0.3), [0,0,0,1])
        set_pose(sd['r_doc_arm_l'], b(sd['doc_x']-0.18, sd['doc_y']-0.22 - 0.04*ctrl, TORSO_Z+0.10), [0,0,0,1])
        set_pose(sd['r_doc_hand_l'], b(sd['doc_x']-0.36, sd['doc_y']-0.30 - 0.04*ctrl, TORSO_Z+0.10), [0,0,0,1])
        set_pose(sd['r_doc_arm_r'], b(sd['doc_x']+0.18, sd['doc_y']-0.22 - 0.04*ctrl2, TORSO_Z+0.10), [0,0,0,1])
        set_pose(sd['r_doc_hand_r'], b(sd['doc_x']+0.36, sd['doc_y']-0.30 - 0.04*ctrl2, TORSO_Z+0.10), [0,0,0,1])
        set_pose(sd['r_doc_torso'], b(sd['doc_x'], sd['doc_y']+sway, TORSO_Z), [0,0,0,1])
        set_pose(sd['r_doc_head'],  b(sd['doc_x'], sd['doc_y']+sway, HEAD_Z),  [0,0,0,1])

    # ── Read Movement Buttons (R1 & R2) ──
    step_size = 0.08 
    moved1 = False; moved2 = False

    r1_l = bb.readDebugParameter('[R1] Left'); r1_r = bb.readDebugParameter('[R1] Right')
    r1_f = bb.readDebugParameter('[R1] Forward'); r1_b = bb.readDebugParameter('[R1] Backward')
    r1_u = bb.readDebugParameter('[R1] Up'); r1_d = bb.readDebugParameter('[R1] Down')
    if r1_l > btn_state['R1_L']: target1_x -= step_size; moved1 = True; btn_state['R1_L'] = r1_l
    if r1_r > btn_state['R1_R']: target1_x += step_size; moved1 = True; btn_state['R1_R'] = r1_r
    if r1_f > btn_state['R1_F']: target1_y += step_size; moved1 = True; btn_state['R1_F'] = r1_f
    if r1_b > btn_state['R1_B']: target1_y -= step_size; moved1 = True; btn_state['R1_B'] = r1_b
    if r1_u > btn_state['R1_U']: target1_z += step_size; moved1 = True; btn_state['R1_U'] = r1_u
    if r1_d > btn_state['R1_D']: target1_z -= step_size; moved1 = True; btn_state['R1_D'] = r1_d

    r2_l = bb.readDebugParameter('[R2] Left'); r2_r = bb.readDebugParameter('[R2] Right')
    r2_f = bb.readDebugParameter('[R2] Forward'); r2_b = bb.readDebugParameter('[R2] Backward')
    r2_u = bb.readDebugParameter('[R2] Up'); r2_d = bb.readDebugParameter('[R2] Down')
    if r2_l > btn_state['R2_L']: target2_x -= step_size; moved2 = True; btn_state['R2_L'] = r2_l
    if r2_r > btn_state['R2_R']: target2_x += step_size; moved2 = True; btn_state['R2_R'] = r2_r
    if r2_f > btn_state['R2_F']: target2_y += step_size; moved2 = True; btn_state['R2_F'] = r2_f
    if r2_b > btn_state['R2_B']: target2_y -= step_size; moved2 = True; btn_state['R2_B'] = r2_b
    if r2_u > btn_state['R2_U']: target2_z += step_size; moved2 = True; btn_state['R2_U'] = r2_u
    if r2_d > btn_state['R2_D']: target2_z -= step_size; moved2 = True; btn_state['R2_D'] = r2_d

    rx = bb.readDebugParameter('rx'); ry = bb.readDebugParameter('ry')
    rz = bb.readDebugParameter('rz'); use_rot = bb.readDebugParameter('use rotation')
    if rx != last_rx or ry != last_ry or rz != last_rz or use_rot != last_use_rot:
        moved1 = True; moved2 = True
        last_rx = rx; last_ry = ry; last_rz = rz; last_use_rot = use_rot

    target1_x = max(-0.95, min(0.8, target1_x)); target1_y = max(0.1, min(1.0, target1_y)) 
    target1_z = max(0.85 if target1_x < -0.2 else 0.28, min(1.2, target1_z)) 

    target2_x = max(OFFSET_X - 0.95, min(OFFSET_X + 0.8, target2_x)); target2_y = max(0.1, min(1.0, target2_y)) 
    target2_z = max(0.85 if (target2_x - OFFSET_X) < -0.2 else 0.28, min(1.2, target2_z)) 

    if moved1 and li > 0:
        quat = bb.getQuaternionFromEuler([rx, ry, rz])
        arm_jpos1 = bb.calculateInverseKinematics(robot1, ee_link, [target1_x, target1_y, target1_z], quat if use_rot else None)
        for i, jp in enumerate(arm_jpos1): bb.setJointMotorControl(robot1, i, targetPosition=jp)
            
    if moved2 and li > 0:
        quat = bb.getQuaternionFromEuler([rx, ry, rz])
        arm_jpos2 = bb.calculateInverseKinematics(robot2, ee_link, [target2_x, target2_y, target2_z], quat if use_rot else None)
        for i, jp in enumerate(arm_jpos2): bb.setJointMotorControl(robot2, i, targetPosition=jp)

    # ── MOVER ROBOT LOGIC (Auto-Drive AGV Cart) ──
    m_f = bb.readDebugParameter('[Mover] Forward (To R2)')
    m_b = bb.readDebugParameter('[Mover] Backward (To R1)')
    m_p = bb.readDebugParameter('[Mover] Pick from Tray')
    m_d = bb.readDebugParameter('[Mover] Drop to Tray')

    # When clicked, set the destination Target
    if m_f > btn_state['M_F']: mover_target_x = 7.10; btn_state['M_F'] = m_f
    if m_b > btn_state['M_B']: mover_target_x = 0.60; btn_state['M_B'] = m_b
    
    # Smooth continuous movement towards the target
    mover_speed = 0.15
    if mover_x < mover_target_x: mover_x = min(mover_x + mover_speed, mover_target_x)
    elif mover_x > mover_target_x: mover_x = max(mover_x - mover_speed, mover_target_x)

    set_pose(mover_base, [mover_x, MOVER_Y, 0.15], [0,0,0,1])
    set_pose(mover_accent, [mover_x, MOVER_Y, 0.20], [0,0,0,1])
    set_pose(mover_w1, [mover_x-0.2, MOVER_Y-0.25, 0.08], [0,0,0,1])
    set_pose(mover_w2, [mover_x+0.2, MOVER_Y-0.25, 0.08], [0,0,0,1])
    set_pose(mover_w3, [mover_x-0.2, MOVER_Y+0.25, 0.08], [0,0,0,1])
    set_pose(mover_w4, [mover_x+0.2, MOVER_Y+0.25, 0.08], [0,0,0,1])
    set_pose(robot3, [mover_x, MOVER_Y, 0.3], bb.getQuaternionFromEuler([0, 0, -math.pi/2]))

    # ── Mover Smart Animated Pick and Drop Logic ──
    # Check if Pick is clicked AND the robot isn't already carrying something
    if m_p > btn_state['M_P']: 
        btn_state['M_P'] = m_p
        if mover_anim_state == 0 and mover_carrying == 0:
            # Check if there is actually a box on the current tray!
            can_pick = False
            if mover_x < 3.85: # At Tray 1
                if box1_loc == 1 or box2_loc == 1: can_pick = True
            else:              # At Tray 2
                if box1_loc == 2 or box2_loc == 2: can_pick = True
            
            # Start animation only if there is a box to grab
            if can_pick:
                mover_anim_state = 1
                mover_anim_timer = 20 # 1 second animation

    # Check if Drop is clicked AND the robot has something to drop
    if m_d > btn_state['M_D']: 
        btn_state['M_D'] = m_d
        if mover_anim_state == 0 and mover_carrying != 0:
            mover_anim_state = 2
            mover_anim_timer = 20

    # Handle the Animation Frame by Frame
    if mover_anim_state != 0:
        mover_anim_timer -= 1
        
        # At exactly the halfway point of the animation, attach/detach the box
        if mover_anim_timer == 10:
            if mover_anim_state == 1: # Picking Action
                if mover_x < 3.85:
                    if box1_loc == 1: mover_carrying = 1; box1_loc = 3
                    elif box2_loc == 1: mover_carrying = 2; box2_loc = 3
                else:
                    if box2_loc == 2: mover_carrying = 2; box2_loc = 3
                    elif box1_loc == 2: mover_carrying = 1; box1_loc = 3
            elif mover_anim_state == 2: # Dropping Action
                target_tray = 1 if mover_x < 3.85 else 2
                if mover_carrying == 1: box1_loc = target_tray
                elif mover_carrying == 2: box2_loc = target_tray
                mover_carrying = 0
                
        # Calculate Blend Factor (1.0 = Fully extended, 0.0 = Retracted)
        if mover_anim_timer > 10: blend = (20 - mover_anim_timer) / 10.0 # Extending out
        else: blend = mover_anim_timer / 10.0                            # Retracting in
            
        if mover_anim_timer <= 0:
            mover_anim_state = 0
            blend = 0.0
            
        # Interpolate between carrying pose and reaching pose
        curr_jpos = [c + (r - c) * blend for c, r in zip(mover_carry_jpos, mover_reach_jpos)]
        for i, jp in enumerate(curr_jpos):
            bb.setJointMotorControl(robot3, i, targetPosition=jp)
    else:
        # Just stay in carrying pose
        for i, jp in enumerate(mover_carry_jpos):
            bb.setJointMotorControl(robot3, i, targetPosition=jp)

    # Move the Transport Boxes to match their states
    try:
        ep3, eq3 = bb.getLinkPose(robot3, ee_link)
        hand_pos = [ep3[0], ep3[1], ep3[2] - 0.05]
        hand_quat = eq3
    except Exception:
        hand_pos = [mover_x, MOVER_Y-0.5, 1.0]
        hand_quat = [0,0,0,1]

    # Box 1 Position Logic
    if box1_loc == 1: set_pose(box1, [0.60, 0.45, 0.56], [0,0,0,1])
    elif box1_loc == 2: set_pose(box1, [7.10, 0.45, 0.56], [0,0,0,1])
    elif box1_loc == 3: set_pose(box1, hand_pos, hand_quat)

    # Box 2 Position Logic (Slightly offset so they don't overlap if dropped on same tray)
    if box2_loc == 1: set_pose(box2, [0.60, 0.35, 0.56], [0,0,0,1])
    elif box2_loc == 2: set_pose(box2, [7.10, 0.45, 0.56], [0,0,0,1])
    elif box2_loc == 3: set_pose(box2, hand_pos, hand_quat)


    # ── Surgical Tool Pick & Drop (R1 & R2) ──
    g1 = bb.readDebugParameter('[R1] Grab Tool'); d1 = bb.readDebugParameter('[R1] Drop Tool')
    if g1 > btn_state['R1_G']: is_grab1 = True; btn_state['R1_G'] = g1
    if d1 > btn_state['R1_Dr']: 
        is_grab1 = False; btn_state['R1_Dr'] = d1
        tool1_p1 = b(setup_data[0]['tx'], setup_data[0]['ty']-0.04, setup_data[0]['tz']-0.222)
        tool1_p2 = b(setup_data[0]['tx'], setup_data[0]['ty']-0.13, setup_data[0]['tz']-0.222)
        tool1_q = [0, 0, 0, 1]

    g2 = bb.readDebugParameter('[R2] Grab Tool'); d2 = bb.readDebugParameter('[R2] Drop Tool')
    if g2 > btn_state['R2_G']: is_grab2 = True; btn_state['R2_G'] = g2
    if d2 > btn_state['R2_Dr']: 
        is_grab2 = False; btn_state['R2_Dr'] = d2
        tool2_p1 = b(setup_data[1]['tx'], setup_data[1]['ty']-0.04, setup_data[1]['tz']-0.222)
        tool2_p2 = b(setup_data[1]['tx'], setup_data[1]['ty']-0.13, setup_data[1]['tz']-0.222)
        tool2_q = [0, 0, 0, 1]

    try:
        ep1, eq1 = bb.getLinkPose(robot1, ee_link)
        ep2, eq2 = bb.getLinkPose(robot2, ee_link)
        
        if is_grab1:
            tool1_p1 = b(ep1[0], ep1[1]+0.09, ep1[2]-0.02); tool1_p2 = b(ep1[0], ep1[1]+0.13, ep1[2]-0.02); tool1_q = eq1
        if is_grab2:
            tool2_p1 = b(ep2[0], ep2[1]+0.09, ep2[2]-0.02); tool2_p2 = b(ep2[0], ep2[1]+0.13, ep2[2]-0.02); tool2_q = eq2
        
        set_pose(setup_data[0]['r_tool'], tool1_p1, tool1_q)
        set_pose(setup_data[0]['r_handle'], tool1_p2, tool1_q)
        set_pose(setup_data[1]['r_tool'], tool2_p1, tool2_q)
        set_pose(setup_data[1]['r_handle'], tool2_p2, tool2_q)
    except Exception:
        pass

    bb.stepSimulation(0.05)
    time.sleep(0.05)
    li += 1