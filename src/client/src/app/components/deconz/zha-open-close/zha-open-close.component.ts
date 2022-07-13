import { Component, OnDestroy, OnInit } from "@angular/core";
import { MessageService } from "primeng/api";
import { Subscription } from "rxjs";
import { Cst } from "src/app/cst";
import { ApiService } from "./api.service";
import { OpenCloseSchema } from "./schemas";

@Component({
    selector: "app-zha-open-close",
    templateUrl: "./zha-open-close.component.html",
})
export class ZhaOpenCloseComponent implements OnInit, OnDestroy {
    private data$: Subscription;
    protected data: OpenCloseSchema | undefined;

    constructor(private api: ApiService, private msg: MessageService) {
        this.data$ = this.api.data("fsf").subscribe({
            next: (value) => {
                this.data = value;
            },
            error: (error) =>
                this.msg.add({
                    severity: Cst.msg.sev_error,
                    summary:
                        "Ошибка получения данных в компоненте ZhaOpenCloseComponent",
                    detail: JSON.stringify(error.message),
                }),
        });
    }

    ngOnInit(): void {}

    ngOnDestroy(): void {
        this.data$.unsubscribe();
    }
}
