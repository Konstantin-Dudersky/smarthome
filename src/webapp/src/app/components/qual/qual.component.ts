import {
    Component,
    Input,
    OnChanges,
    OnInit,
    SimpleChanges,
} from "@angular/core";
import { Qual } from "src/app/shemas/siganals";
import { Cst } from "src/app/cst";

@Component({
    selector: "app-qual",
    templateUrl: "./qual.component.html",
})
export class QualComponent implements OnInit, OnChanges {
    @Input()
    qual: Qual | undefined;

    protected cst = Cst;
    protected severity: string = Cst.tag.sev_info;
    protected visible: boolean = false;

    constructor() {}

    ngOnInit(): void {}

    ngOnChanges(changes: SimpleChanges): void {
        if (this.qual == undefined) return;
        switch (Number(this.qual)) {
            case Qual.BAD:
                this.visible = true;
                this.severity = Cst.tag.sev_danger;
                break;
            case Qual.GOOD:
                this.visible = false;
                this.severity = Cst.tag.sev_info;
                break;

            default:
                break;
        }
    }
}
