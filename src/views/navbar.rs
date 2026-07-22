use crate::Route;
use dioxus::prelude::*;

const NAVBAR_CSS: Asset = asset!("/assets/styling/navbar.css");

/// Shared tab navigation wrapping every page.
#[component]
pub fn Navbar() -> Element {
    rsx! {
        document::Link { rel: "stylesheet", href: NAVBAR_CSS }

        nav {
            id: "navbar",
            Link {
                to: Route::Me {},
                active_class: "active",
                "Me"
            }
            Link {
                to: Route::Dialogue {},
                active_class: "active",
                "Dialogue"
            }
            Link {
                to: Route::Misc {},
                active_class: "active",
                "Misc"
            }
        }

        Outlet::<Route> {}
    }
}
