use dioxus::prelude::*;

/// Placeholder for the Matter page (renamed from “me”).
#[component]
pub fn Matter() -> Element {
    rsx! {
        div {
            id: "matter",
            h1 { "Matter" }
            p { "This page is a placeholder for Matter." }
        }
    }
}
