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
import { SigFloat } from "src/app/shemas/siganals";

@Component({
    selector: "app-oa-analog",
    templateUrl: "./oa-analog.component.html",
})
export class OaAnalogComponent implements OnInit, OnChanges {
    @Input()
    signal: SigFloat | undefined;
    @Output()
    newValue = new EventEmitter<number>();

    protected cst = Cst;
    protected visible: boolean = false;
    protected form = new FormGroup({
        value: new FormControl(0, {
            nonNullable: true,
        }),
    });
    constructor() {}

    ngOnInit(): void {}

    ngOnChanges(changes: SimpleChanges): void {
        if (!this.signal) return;
        if (this.form.pristine)
            this.form.controls.value.setValue(this.signal.value);
    }

    open() {
        this.visible = true;
    }

    protected onHide() {
        this.form.markAsPristine();
    }

    protected ok() {
        if (this.form.invalid) {
            return;
        }
        this.newValue.emit(this.form.controls.value.value);
        this.visible = false;
    }

    protected cancel() {
        this.visible = false;
    }
}
