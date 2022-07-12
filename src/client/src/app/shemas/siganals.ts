export enum Qual {
    BAD = 0,
    GOOD = 80,
}

export enum Units {
    "K" = 1000,
    "℃" = 1001,
    "%" = 1342,
}

export interface SigBool {
    value: boolean;
    qual: Qual;
}

export interface Scale {
    low: number;
    high: number;
}

export interface SigFloat {
    value: number;
    unit: Units;
    qual: Qual;
    scale: Scale;
}
