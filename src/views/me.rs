use crate::components::{Echo, Hero};
use dioxus::prelude::*;

/// The Me tab — default landing page.
#[component]
pub fn Me() -> Element {
    rsx! {
        div {
            id: "me",
            Hero {}
            Echo {}
        }
    }
}
