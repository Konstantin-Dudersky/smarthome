import { Component, OnDestroy, OnInit } from "@angular/core";
import { MessageService } from "primeng/api";
import { Subscription } from "rxjs";
import { Cst } from "src/app/cst";
import { ApiService } from "./api.service";
import { ZHAPressureSchema } from "./schemas";

@Component({
    selector: "app-zha-pressure",
    templateUrl: "./zha-pressure.component.html",
})
export class ZhaPressureComponent implements OnInit, OnDestroy {
    private data$: Subscription;
    protected data: ZHAPressureSchema | undefined;

    constructor(private api: ApiService, private msg: MessageService) {
        this.data$ = this.api.data("fsf").subscribe({
            next: (value) => {
                this.data = value;
            },
            error: (error) =>
                this.msg.add({
                    severity: Cst.msg.sev_error,
                    summary:
                        "Ошибка получения данных в компоненте ZhaPressureComponent",
                    detail: JSON.stringify(error.message),
                }),
        });
    }

    ngOnInit(): void {}

    ngOnDestroy(): void {
        this.data$.unsubscribe();
    }
}
