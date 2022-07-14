import { AppRoutingModule } from "./app-routing.module";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { BrowserModule } from "@angular/platform-browser";
import { HttpClientModule } from "@angular/common/http";
import { NgModule } from "@angular/core";
import { ReactiveFormsModule } from "@angular/forms";
// components ------------------------------------------------------------------
import { AppComponent } from "./app.component";
import { QualComponent } from "./components/qual/qual.component";
import { SigBoolComponent } from "./components/sig-bool/sig-bool.component";
import { SigFloatComponent } from "./components/sig-float/sig-float.component";
import { YeelightComponent } from "./yeelight/component/yeelight.component";
import { OaAnalogComponent } from "./components/oa/oa-analog/oa-analog.component";
import { ZhaOpenCloseComponent } from "./components/deconz/zha-open-close/zha-open-close.component";
// primeng ---------------------------------------------------------------------
import { AvatarModule } from "primeng/avatar";
import { ButtonModule } from "primeng/button";
import { DialogModule } from "primeng/dialog";
import { InputNumberModule } from "primeng/inputnumber";
import { InputSwitchModule } from "primeng/inputswitch";
import { MessageService } from "primeng/api";
import { SkeletonModule } from "primeng/skeleton";
import { SliderModule } from "primeng/slider";
import { TagModule } from "primeng/tag";
import { ToastModule } from "primeng/toast";

@NgModule({
    declarations: [
        AppComponent,
        YeelightComponent,
        SigBoolComponent,
        QualComponent,
        SigFloatComponent,
        OaAnalogComponent,
        ZhaOpenCloseComponent,
    ],
    imports: [
        AppRoutingModule,
        BrowserModule,
        BrowserAnimationsModule,
        HttpClientModule,
        ReactiveFormsModule,
        // primeng -------------------------------------------------------------
        AvatarModule,
        ButtonModule,
        DialogModule,
        InputNumberModule,
        InputSwitchModule,
        SkeletonModule,
        SliderModule,
        TagModule,
        ToastModule,
    ],
    providers: [MessageService],
    bootstrap: [AppComponent],
})
export class AppModule {}
