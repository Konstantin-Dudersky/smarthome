import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, repeat } from "rxjs";
import { ZHAPressureSchema } from "./schemas";

@Injectable({
    providedIn: "root",
})
export class ApiService {
    IP = `http://${window.location.hostname}/api`;

    constructor(private http: HttpClient) {}

    data(deviceId: string): Observable<ZHAPressureSchema> {
        return this.http
            .get<ZHAPressureSchema>(
                `${this.IP}/devices/deconz/zhapressure/${deviceId}`
            )
            .pipe(repeat({ delay: 500 }));
    }
}
