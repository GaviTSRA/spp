from .nodes import *

NODES = {
    # BEGIN START EVENT
    "flag_clicked": "event_whenflagclicked", 
    "key_pressed": "event_whenkeypressed",
    "sprite_clicked": "event_whenthisspriteclicked",
    # BEGIN MOTION
    "move": "motion_movesteps",
    "rturn": "motion_turnright",
    "lturn": "motion_turnleft",
    "setx": "motion_setx",
    "sety": "motion_sety",
    "changex": "motion_changexby",
    "changey": "motion_changeyby",
    # START LOOKS
    # START SOUND
    # START EVENTS
    # START CONTROL
    "wait": "control_wait",
    # START SENSING
    # START OPERATORS
    # START VARIABLES
    # START MYBLOCKS
}
UNSUPPORTED_NODES = {
    # BEGIN START EVENT
    "backdrop_switch_to": "event_whenbackdropswitchesto",
    "greater_then": "event_whengreaterthan",
    "broadcast_received": "event_whenbroadcastreceived",
    # BEGIN MOTION
    "goto": "motion_goto",       #motion_goto_menu
    "gotoxy": "motion_gotoxy",
    "glide": "motion_glideto",   #motion_glideto_menu
    "glidexy": "motion_glidetoxy",
    "point": "motion_point_in_direction",
    "pointto": "motion_pointtowardsmotion_pointtowards", #motion_pointtowards_menu
    "edgebounce": "motion_ifonedgebounce",
    "rotstyle": "motion_setrotationstyle",
    # START LOOKS
    "say_for": "looks_sayforsecs",
    "say": "looks_say",
    "think_for": "looks_thinkforsecs",
    "think": "looks_think",
    "costume_switch_to": "looks_switchcostumeto",  #looks_costume
    "next_costume": "looks_nextcostume",
    "backdrop_switch_to": "looks_switchbackdropto", #looks_backdrops
    "next_backdrop": "looks_nextbackdrop",
    "change_size_by": "looks_changesizeby",
    "set_size": "looks_setsizeto",
    "change_effect_by": "looks_changeeffectby",
    "set_effect": "looks_seteffectto",
    "clear_effects": "looks_cleargraphiceffects",
    "show": "looks_show",
    "hide": "looks_hide",
    "go_to_layer": "looks_gotofrontback",
    "go_layers_forward": "looks_goforwardbackwardlayers",
    # START SOUND
    "play_sound_until_done": "sound_playuntildone", #sound_sounds_menu
    "play_sound": "sound_play", #sound_sounds_menu
    "stop_all_sounds": "sound_stopallsounds",
    "change_effect_by": "sound_changeeffectby",
    "set_effect": "sound_seteffectto",
    "clear_effects": "sound_cleareffects",
    "change_volume": "sound_changevolumeby",
    "set_volume": "sound_setvolumeto",
    # START EVENTS
    "broadcast": "event_broadcast",
    "broadcast_wait": "event_broadcastandwait",
    # START CONTROL
    "repeat": "control_repeat",
    "forever": "control_forever",
    "if": "control_if",
    "ife": "control_if_else",
    "wait_until": "control_wait_until",
    "repeat_until": "control_repeat_until",
    "stop": "control_stop",
    "start_clone": "control_start_as_clone",
    "create_clone": "control_create_clone_of", #control_create_clone_of_menu
    "delete_clone": "control_delete_this_clone",
    # START SENSING
    #TODO
    # START OPERATORS
    #TODO
    # START VARIABLES
    #TODO
    # START MYBLOCKS
    #TODO
}

class Compiler:
    def __init__(self):
        self.res = ""
        self.index = 0

    def visit(self, node):
        method_name = f'visit_' + type(node).__name__
        method = getattr(self, method_name)
        return method(node)

    def visit_FileNode(self, node):
        self.res = '"blocks":{'
        for block in node.blocks:
            self.visit(block)
        self.res += "},"
        return self.res

    def visit_BlockNode(self, node):
        self.visit(node.start_condition)
        self.visit(node.body)

    def visit_StartConditionNode(self, node):
        result = "," if node.index > 0 else ""

        result += f'"{node.index}": ' + "{"
        try:
            result += f'"opcode": "{NODES[node.start_condition.lower()]}",'
        except:
            raise ValueError("Action not found or not supported: " + node.start_condition)
        result += f'"next": "{node.next}",' if node.next != None else '"next": null,'
        result += f'"parent": null,'
        result += '"inputs": {},'
        if node.start_condition.lower() in ["key_pressed"]:
            result += '"fields": {"KEY_OPTION":["' + node.arg + '", null]},'
        else: result += '"fields": {},'
        result += '"shadow": false,'
        result += '"topLevel": true'
        result += "}"
        
        self.res += result

    def visit_BodyNode(self, node):
        for expr in node.exprs:
            self.visit(expr)

    def visit_ExprNode(self, node):
        result = ""

        result += f',"{node.index}": ' + "{"
        try:
            result += f'"opcode": "{NODES[node.instr.value.lower()]}",'
        except:
            raise ValueError("Action not found or not supported: " + node.instr.value)
        result += f'"next": "{node.next}",' if node.next != None else '"next": null,'
        result += f'"parent": ' + f'"{node.previous}",' if node.previous != None else "null,"

        if node.instr.value.lower() in ["move"]:
            result += '"inputs": {"STEPS": [1,[4,'
            if node.value == None:
                raise ValueError("move instruction needs one value")
            result += f'"{node.value}"' + ']]},'
        elif node.instr.value.lower() in ["lturn", "rturn"]:
            result += '"inputs": {"DEGREES": [1,[4,'
            if node.value == None:
                raise ValueError("turn instruction needs one value")
            result += f'"{node.value}"' + ']]},'
        elif node.instr.value.lower() in ["wait"]:
            result += '"inputs": {"DURATION": [1,[5,'
            if node.value == None:
                raise ValueError("turn instruction needs one value")
            result +=  f'"{node.value}"' + ']]},'
        elif node.instr.value.lower() in ["setx"]:
            result += '"inputs": {"X": [1,[4,'
            if node.value == None:
                raise ValueError("turn instruction needs one value")
            result +=  f'"{node.value}"' + ']]},'
        elif node.instr.value.lower() in ["sety"]:
            result += '"inputs": {"Y": [1,[4,'
            if node.value == None:
                raise ValueError("turn instruction needs one value")
            result +=  f'"{node.value}"' + ']]},'
        elif node.instr.value.lower() in ["changex"]:
            result += '"inputs": {"DX": [1,[4,'
            if node.value == None:
                raise ValueError("turn instruction needs one value")
            result +=  f'"{node.value}"' + ']]},'
        elif node.instr.value.lower() in ["changey"]:
            result += '"inputs": {"DY": [1,[4,'
            if node.value == None:
                raise ValueError("turn instruction needs one value")
            result +=  f'"{node.value}"' + ']]},'

        result += '"fields": {},"shadow": false,"topLevel": false}'

        self.res += result

    def visit_IfNode(self, node):
        result = ""

        result += f',"{node.index}": ' + '{"opcode": "control_if","next": null,"parent": null,"inputs": {'
        result += f'"CONDITION": [2,'
        result += '"xdu%=xh(Ocq^JRS+]kK["' # TODO if conditions
        result += '],"SUBSTACK": [2,'

        for n in node.body.exprs:
            result += f'"{n.index}",'
        result = result[:-1]

        result += ']},"fields": {},"shadow": false,"topLevel": false}'
        
        self.res += result
        self.visit(node.body)