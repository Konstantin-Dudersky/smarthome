import { SigBool, SigFloat } from "../shemas/siganals";

export interface Yeelight {
    power: SigBool;
    bright: SigFloat;
    color_mode: SigFloat;
    ct: SigFloat;
    rgb: SigFloat;
}
