import { Component, Input, OnInit } from "@angular/core";

@Component({
    selector: "app-sig-float",
    templateUrl: "./sig-float.component.html",
})
export class SigFloatComponent implements OnInit {
    @Input()
    label: string = "Label";

    constructor() {}

    ngOnInit(): void {}
}
