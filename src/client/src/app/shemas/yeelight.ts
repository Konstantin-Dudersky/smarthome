import { SigBool, SigFloat } from "./siganals";

export interface Yeelight {
  power: SigBool;
  bright: SigFloat;
}
