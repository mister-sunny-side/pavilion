use crate::blog_book::BookRoute;
use crate::Route;
use dioxus::prelude::*;

/// Link from the dialogue index (or elsewhere) to a compiled markdown post.
#[component]
pub fn PostLink(route: BookRoute) -> Element {
    rsx! {
        Link {
            to: Route::DialoguePost { child: route },
            "{route.page().title}"
        }
    }
}

/// Link back to the dialogue post index.
#[component]
pub fn DialogueIndexLink(
    #[props(default = "Back to dialogue".to_string())] label: String,
) -> Element {
    rsx! {
        Link {
            to: Route::Dialogue {},
            class: "dialogue-back",
            "{label}"
        }
    }
}
