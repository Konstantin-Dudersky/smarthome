import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, repeat } from "rxjs";
import { ZHAHumiditySchema } from "./schemas";

@Injectable({
    providedIn: "root",
})
export class ApiService {
    IP = `http://${window.location.hostname}/api`;

    constructor(private http: HttpClient) {}

    data(deviceId: string): Observable<ZHAHumiditySchema> {
        return this.http
            .get<ZHAHumiditySchema>(
                `${this.IP}/devices/deconz/zhahumidity/${deviceId}`
            )
            .pipe(repeat({ delay: 500 }));
    }
}
