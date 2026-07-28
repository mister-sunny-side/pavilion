use crate::components::{DialogueIndexLink, PostList};
use crate::Route;
use dioxus::prelude::*;

const DIALOGUE_CSS: Asset = asset!("/assets/styling/dialogue.css");

/// Post index for markdown pages under `blog-posts/`.
#[component]
pub fn Dialogue() -> Element {
    rsx! {
        document::Link { rel: "stylesheet", href: DIALOGUE_CSS }

        div {
            id: "dialogue",
            class: "page",
            h1 { "Dialogue" }
            p { "Posts compiled from markdown at build time." }
            PostList {}
        }
    }
}

/// Layout wrapper around a single generated blog post page.
#[component]
pub fn DialoguePost() -> Element {
    rsx! {
        document::Link { rel: "stylesheet", href: DIALOGUE_CSS }

        div {
            id: "dialogue-post",
            class: "page",
            DialogueIndexLink {}
            article { class: "dialogue-article markdown-body",
                Outlet::<Route> {}
            }
        }
    }
}
