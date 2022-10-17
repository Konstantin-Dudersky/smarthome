import {
    Component,
    EventEmitter,
    Input,
    OnChanges,
    OnInit,
    Output,
    SimpleChanges,
} from "@angular/core";
import { FormControl, FormGroup } from "@angular/forms";
import { Cst } from "src/app/cst";
import { SigFloat, Units } from "src/app/shemas/siganals";

@Component({
    selector: "app-sig-float",
    templateUrl: "./sig-float.component.html",
})
export class SigFloatComponent implements OnInit, OnChanges {
    @Input()
    label: string = "Label";
    @Input()
    signal!: SigFloat;
    @Output()
    popup = new EventEmitter<null>();

    protected units = Units;
    protected cst = Cst;
    protected form = new FormGroup({
        value: new FormControl<number>(0),
    });

    constructor() {}

    ngOnInit(): void {}

    ngOnChanges(changes: SimpleChanges): void {
        if (!this.signal) return;
        this.form.controls.value.setValue(this.signal.value);
    }
}
