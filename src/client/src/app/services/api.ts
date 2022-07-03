import { Injectable } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Yeelight } from "../shemas/yeelight";
import { Observable, repeat } from "rxjs";

@Injectable({
    providedIn: "root",
})
export class ApiService {
    IP = `http://${window.location.hostname}/api`;

    constructor(private http: HttpClient) {}

    yeelight(device_id: string): Observable<Yeelight> {
        return this.http
            .get<Yeelight>(`${this.IP}/devices/yeelight/${device_id}`)
            .pipe(repeat({ delay: 500 }));
    }

    setPower(device_id: string, power: boolean): Observable<null> {
        return this.http.get<null>(
            `${this.IP}/devices/yeelight/${device_id}/set-power`,
            { params: new HttpParams().set("power", power) }
        );
    }
}
