export enum Qual {
  BAD = 0,
  GOOD = 80,
}

export interface SigBool {
  value: boolean;
  qual: Qual;
}

export interface SigFloat {
  value: number;
  unit: number;
  qual: Qual;
}
