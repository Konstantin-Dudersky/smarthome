import {
    Component,
    Input,
    OnChanges,
    OnDestroy,
    OnInit,
    SimpleChanges,
} from "@angular/core";
import { Subscription } from "rxjs";
import { YeelightService } from "../services";
import { Yeelight } from "../shemas";

@Component({
    selector: "app-yeelight",
    templateUrl: "./yeelight.component.html",
})
export class YeelightComponent implements OnInit, OnDestroy, OnChanges {
    @Input()
    device_id: string = "";

    private data$ = new Subscription();
    protected data: Yeelight = <Yeelight>{};
    protected dialogPower = false;
    private setPower$ = new Subscription();
    private setBright$ = new Subscription();
    private setCt$ = new Subscription();
    private setRgb$ = new Subscription();
    private subs: Subscription[] = [
        this.data$,
        this.setPower$,
        this.setBright$,
        this.setCt$,
        this.setRgb$,
    ];
    constructor(private api: YeelightService) {}

    ngOnInit(): void {}

    ngOnChanges(changes: SimpleChanges): void {
        this.data$ = this.api.yeelight(this.device_id).subscribe({
            next: (data) => {
                this.data = data;
            },
        });
    }

    ngOnDestroy(): void {
        this.subs.forEach((sub) => sub.unsubscribe());
    }

    protected setPower(power: boolean): void {
        this.setPower$ = this.api.setPower(this.device_id, power).subscribe();
    }

    protected setBright(bright: number): void {
        this.setBright$ = this.api.setBright(this.device_id, bright).subscribe({
            error: (error) => console.error(error),
        });
    }

    protected setCt(ctValue: number): void {
        this.setCt$ = this.api.setCt(this.device_id, ctValue).subscribe({
            error: (error) => console.error(error),
        });
    }

    protected setRgb(rgbValue: number): void {
        this.setRgb$ = this.api.setRgb(this.device_id, rgbValue).subscribe({
            error: (error) => console.error(error),
        });
    }
}
