import { Injectable } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";

@Injectable({
    providedIn: "root",
})
export class ApiService {
    IP = `http://${window.location.hostname}/api`;

    constructor(private http: HttpClient) {}
}
