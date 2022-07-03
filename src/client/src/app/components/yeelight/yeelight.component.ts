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

    constructor(private api: ApiService) {}

    ngOnInit(): void {}

    ngOnChanges(changes: SimpleChanges): void {
        this.data$ = this.api.yeelight(this.device_id).subscribe({
            next: (data) => {
                this.data = data;
            },
        });
    }

    protected setPower(power: boolean): void {
        this.setPower$ = this.api.setPower(this.device_id, power).subscribe();
    }

    ngOnDestroy(): void {
        this.data$.unsubscribe();
        this.setPower$.unsubscribe();
    }
}
