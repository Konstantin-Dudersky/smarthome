import { Injectable } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Yeelight } from "../yeelight/shemas";
import { Observable, repeat } from "rxjs";

@Injectable({
    providedIn: "root",
})
export class YeelightService {
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

    setBright(device_id: string, bright: number): Observable<null> {
        return this.http.get<null>(
            `${this.IP}/devices/yeelight/${device_id}/set-bright`,
            { params: new HttpParams().set("bright", bright) }
        );
    }

    setCt(device_id: string, ctValue: number): Observable<null> {
        return this.http.get<null>(
            `${this.IP}/devices/yeelight/${device_id}/set-ct`,
            { params: new HttpParams().set("ctValue", ctValue) }
        );
    }

    setRgb(device_id: string, rgbValue: number): Observable<null> {
        return this.http.get<null>(
            `${this.IP}/devices/yeelight/${device_id}/set-rgb`,
            { params: new HttpParams().set("rgbValue", rgbValue) }
        );
    }
}
