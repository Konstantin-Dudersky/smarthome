'use strict';

customElements.define('compodoc-menu', class extends HTMLElement {
    constructor() {
        super();
        this.isNormalMode = this.getAttribute('mode') === 'normal';
    }

    connectedCallback() {
        this.render(this.isNormalMode);
    }

    render(isNormalMode) {
        let tp = lithtml.html(`
        <nav>
            <ul class="list">
                <li class="title">
                    <a href="index.html" data-type="index-link">client documentation</a>
                </li>

                <li class="divider"></li>
                ${ isNormalMode ? `<div id="book-search-input" role="search"><input type="text" placeholder="Type to search"></div>` : '' }
                <li class="chapter">
                    <a data-type="chapter-link" href="index.html"><span class="icon ion-ios-home"></span>Getting started</a>
                    <ul class="links">
                        <li class="link">
                            <a href="overview.html" data-type="chapter-link">
                                <span class="icon ion-ios-keypad"></span>Overview
                            </a>
                        </li>
                        <li class="link">
                            <a href="index.html" data-type="chapter-link">
                                <span class="icon ion-ios-paper"></span>README
                            </a>
                        </li>
                                <li class="link">
                                    <a href="dependencies.html" data-type="chapter-link">
                                        <span class="icon ion-ios-list"></span>Dependencies
                                    </a>
                                </li>
                                <li class="link">
                                    <a href="properties.html" data-type="chapter-link">
                                        <span class="icon ion-ios-apps"></span>Properties
                                    </a>
                                </li>
                    </ul>
                </li>
                    <li class="chapter modules">
                        <a data-type="chapter-link" href="modules.html">
                            <div class="menu-toggler linked" data-toggle="collapse" ${ isNormalMode ?
                                'data-target="#modules-links"' : 'data-target="#xs-modules-links"' }>
                                <span class="icon ion-ios-archive"></span>
                                <span class="link-name">Modules</span>
                                <span class="icon ion-ios-arrow-down"></span>
                            </div>
                        </a>
                        <ul class="links collapse " ${ isNormalMode ? 'id="modules-links"' : 'id="xs-modules-links"' }>
                            <li class="link">
                                <a href="modules/AppModule.html" data-type="entity-link" >AppModule</a>
                                    <li class="chapter inner">
                                        <div class="simple menu-toggler" data-toggle="collapse" ${ isNormalMode ?
                                            'data-target="#components-links-module-AppModule-ee0de97e7bd965de762a89eccb1407a944a04acc85b789b4f46960674b1b0f997730a145bea63bd5893a471a370ae4cb90df69f1879128f1b3fe275f4ae1c333"' : 'data-target="#xs-components-links-module-AppModule-ee0de97e7bd965de762a89eccb1407a944a04acc85b789b4f46960674b1b0f997730a145bea63bd5893a471a370ae4cb90df69f1879128f1b3fe275f4ae1c333"' }>
                                            <span class="icon ion-md-cog"></span>
                                            <span>Components</span>
                                            <span class="icon ion-ios-arrow-down"></span>
                                        </div>
                                        <ul class="links collapse" ${ isNormalMode ? 'id="components-links-module-AppModule-ee0de97e7bd965de762a89eccb1407a944a04acc85b789b4f46960674b1b0f997730a145bea63bd5893a471a370ae4cb90df69f1879128f1b3fe275f4ae1c333"' :
                                            'id="xs-components-links-module-AppModule-ee0de97e7bd965de762a89eccb1407a944a04acc85b789b4f46960674b1b0f997730a145bea63bd5893a471a370ae4cb90df69f1879128f1b3fe275f4ae1c333"' }>
                                            <li class="link">
                                                <a href="components/AppComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >AppComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/OaAnalogComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >OaAnalogComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/QualComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >QualComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/SigBoolComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >SigBoolComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/SigFloatComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >SigFloatComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/YeelightComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >YeelightComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/ZhaHumidityComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ZhaHumidityComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/ZhaOpenCloseComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ZhaOpenCloseComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/ZhaPressureComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ZhaPressureComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/ZhaTemperatureComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ZhaTemperatureComponent</a>
                                            </li>
                                        </ul>
                                    </li>
                            </li>
                            <li class="link">
                                <a href="modules/AppRoutingModule.html" data-type="entity-link" >AppRoutingModule</a>
                            </li>
                </ul>
                </li>
                        <li class="chapter">
                            <div class="simple menu-toggler" data-toggle="collapse" ${ isNormalMode ? 'data-target="#injectables-links"' :
                                'data-target="#xs-injectables-links"' }>
                                <span class="icon ion-md-arrow-round-down"></span>
                                <span>Injectables</span>
                                <span class="icon ion-ios-arrow-down"></span>
                            </div>
                            <ul class="links collapse " ${ isNormalMode ? 'id="injectables-links"' : 'id="xs-injectables-links"' }>
                                <li class="link">
                                    <a href="injectables/ApiService.html" data-type="entity-link" >ApiService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/ApiService-1.html" data-type="entity-link" >ApiService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/ApiService-2.html" data-type="entity-link" >ApiService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/ApiService-3.html" data-type="entity-link" >ApiService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/ApiService-4.html" data-type="entity-link" >ApiService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/YeelightService.html" data-type="entity-link" >YeelightService</a>
                                </li>
                            </ul>
                        </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-toggle="collapse" ${ isNormalMode ? 'data-target="#interfaces-links"' :
                            'data-target="#xs-interfaces-links"' }>
                            <span class="icon ion-md-information-circle-outline"></span>
                            <span>Interfaces</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? ' id="interfaces-links"' : 'id="xs-interfaces-links"' }>
                            <li class="link">
                                <a href="interfaces/OpenCloseSchema.html" data-type="entity-link" >OpenCloseSchema</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Scale.html" data-type="entity-link" >Scale</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/SigBool.html" data-type="entity-link" >SigBool</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/SigFloat.html" data-type="entity-link" >SigFloat</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Yeelight.html" data-type="entity-link" >Yeelight</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ZHAHumiditySchema.html" data-type="entity-link" >ZHAHumiditySchema</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ZHAPressureSchema.html" data-type="entity-link" >ZHAPressureSchema</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ZHATemperatureSchema.html" data-type="entity-link" >ZHATemperatureSchema</a>
                            </li>
                        </ul>
                    </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-toggle="collapse" ${ isNormalMode ? 'data-target="#miscellaneous-links"'
                            : 'data-target="#xs-miscellaneous-links"' }>
                            <span class="icon ion-ios-cube"></span>
                            <span>Miscellaneous</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="miscellaneous-links"' : 'id="xs-miscellaneous-links"' }>
                            <li class="link">
                                <a href="miscellaneous/enumerations.html" data-type="entity-link">Enums</a>
                            </li>
                            <li class="link">
                                <a href="miscellaneous/variables.html" data-type="entity-link">Variables</a>
                            </li>
                        </ul>
                    </li>
                        <li class="chapter">
                            <a data-type="chapter-link" href="routes.html"><span class="icon ion-ios-git-branch"></span>Routes</a>
                        </li>
                    <li class="chapter">
                        <a data-type="chapter-link" href="coverage.html"><span class="icon ion-ios-stats"></span>Documentation coverage</a>
                    </li>
                    <li class="divider"></li>
                    <li class="copyright">
                        Documentation generated using <a href="https://compodoc.app/" target="_blank">
                            <img data-src="images/compodoc-vectorise.png" class="img-responsive" data-type="compodoc-logo">
                        </a>
                    </li>
            </ul>
        </nav>
        `);
        this.innerHTML = tp.strings;
    }
});