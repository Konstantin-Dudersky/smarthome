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
import { SigBool } from "src/app/shemas/siganals";
import { Cst } from "src/app/cst";

@Component({
    selector: "app-sig-bool",
    templateUrl: "./sig-bool.component.html",
})
export class SigBoolComponent implements OnInit, OnChanges {
    @Input()
    label: string = "Label";
    @Input()
    signal: SigBool | undefined;
    @Output()
    onClick: EventEmitter<null> = new EventEmitter();

    protected cst = Cst;

    protected form = new FormGroup({
        value: new FormControl<boolean>(false),
    });

    constructor() {}

    ngOnInit(): void {}

    ngOnChanges(changes: SimpleChanges): void {
        if (!this.signal) return;
        this.form.controls.value.setValue(this.signal.value);
    }

    protected click(): void {
        this.onClick.emit();
    }
}
