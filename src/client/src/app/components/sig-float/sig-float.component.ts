import {
    Component,
    EventEmitter,
    Input,
    OnChanges,
    OnInit,
    Output,
    SimpleChanges,
} from "@angular/core";
import { Cst } from "src/app/cst";
import { SigFloat } from "src/app/shemas/siganals";

@Component({
    selector: "app-sig-float",
    templateUrl: "./sig-float.component.html",
})
export class SigFloatComponent implements OnInit, OnChanges {
    @Input()
    label: string = "Label";
    @Input()
    signal: SigFloat | undefined;
    @Output()
    onClick: EventEmitter<null> = new EventEmitter();

    protected cst = Cst;

    constructor() {}

    ngOnInit(): void {}

    ngOnChanges(changes: SimpleChanges): void {
        throw new Error("Method not implemented.");
    }
}
