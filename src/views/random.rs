use dioxus::prelude::*;

/// Placeholder for the Random page (renamed from “misc”).
#[component]
pub fn Random() -> Element {
    rsx! {
        div {
            id: "random",
            h1 { "Random" }
            p { "This page is a placeholder for Random." }
        }
    }
}
