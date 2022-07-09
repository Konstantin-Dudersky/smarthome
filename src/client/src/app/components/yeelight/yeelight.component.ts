import {
    Component,
    Input,
    OnChanges,
    OnDestroy,
    OnInit,
    SimpleChanges,
} from "@angular/core";
import { Subscription } from "rxjs";
import { ApiService } from "src/app/services/api";
import { Yeelight } from "src/app/shemas/yeelight";

@Component({
    selector: "app-yeelight",
    templateUrl: "./yeelight.component.html",
})
export class YeelightComponent implements OnInit, OnDestroy, OnChanges {
    @Input()
    device_id: string = "";

    private data$: Subscription = new Subscription();
    protected data: Yeelight = <Yeelight>{};
    protected dialogPower: boolean = false;
    private setPower$: Subscription = new Subscription();
    private setBright$: Subscription = new Subscription();
    private subs: Subscription[] = [
        this.data$,
        this.setPower$,
        this.setBright$,
    ];
    constructor(private api: ApiService) {}

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
}
