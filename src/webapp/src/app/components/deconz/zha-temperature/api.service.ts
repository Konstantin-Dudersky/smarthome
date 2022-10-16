import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, repeat } from "rxjs";
import { ZHATemperatureSchema } from "./schemas";

@Injectable({
    providedIn: "root",
})
export class ApiService {
    IP = `http://${window.location.hostname}/api`;

    constructor(private http: HttpClient) {}

    data(deviceId: string): Observable<ZHATemperatureSchema> {
        return this.http
            .get<ZHATemperatureSchema>(
                `${this.IP}/devices/deconz/zhatemperature/${deviceId}`
            )
            .pipe(repeat({ delay: 500 }));
    }
}
