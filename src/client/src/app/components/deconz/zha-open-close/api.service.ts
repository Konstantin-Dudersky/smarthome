import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, repeat } from "rxjs";
import { OpenCloseSchema } from "./schemas";

@Injectable({
    providedIn: "root",
})
export class ApiService {
    IP = `http://${window.location.hostname}/api`;

    constructor(private http: HttpClient) {}

    data(deviceId: string): Observable<OpenCloseSchema> {
        return this.http
            .get<OpenCloseSchema>(
                `${this.IP}/devices/deconz/zhaopenclose/${deviceId}`
            )
            .pipe(repeat({ delay: 500 }));
    }
}
