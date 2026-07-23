use crate::Route;
use dioxus::prelude::*;

const NAVBAR_CSS: Asset = asset!("/assets/styling/navbar.css");

/// Shared layout navbar for all top-level routes.
#[component]
pub fn Navbar() -> Element {
    rsx! {
        document::Link { rel: "stylesheet", href: NAVBAR_CSS }

        div {
            id: "navbar",
            Link {
                to: Route::Home {},
                "Home"
            }
            Link {
                to: Route::Dialogue {},
                "Dialogue"
            }
            Link {
                to: Route::Matter {},
                "Matter"
            }
            Link {
                to: Route::Random {},
                "Random"
            }
        }

        Outlet::<Route> {}
    }
}
