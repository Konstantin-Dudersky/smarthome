import { Component, OnDestroy, OnInit } from "@angular/core";
import { MessageService } from "primeng/api";
import { Subscription } from "rxjs";
import { Cst } from "src/app/cst";
import { ApiService } from "./api.service";
import { ZHATemperatureSchema } from "./schemas";

@Component({
    selector: "app-zha-temperature",
    templateUrl: "./zha-temperature.component.html",
})
export class ZhaTemperatureComponent implements OnInit, OnDestroy {
    private data$: Subscription;
    protected data: ZHATemperatureSchema | undefined;

    constructor(private api: ApiService, private msg: MessageService) {
        this.data$ = this.api.data("fsf").subscribe({
            next: (value) => {
                this.data = value;
            },
            error: (error) =>
                this.msg.add({
                    severity: Cst.msg.sev_error,
                    summary:
                        "Ошибка получения данных в компоненте ZhaHumidityComponent",
                    detail: JSON.stringify(error.message),
                }),
        });
    }

    ngOnInit(): void {}

    ngOnDestroy(): void {
        this.data$.unsubscribe();
    }
}
