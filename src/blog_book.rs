#![allow(dead_code)]

//! Build-time generated mdBook router for `blog-posts/`.
//!
//! `BookRoute` and per-page components are produced by `mdbook-gen` in `build.rs`.

use dioxus::prelude::*;

/// Fenced code blocks in markdown expand to this component.
#[component]
pub fn CodeBlock(source: String, language: String, name: Option<String>) -> Element {
    rsx! {
        div {
            class: "code-block border overflow-hidden rounded-md my-4",
            "data-codeblock": "true",
            if let Some(path) = name.as_ref() {
                div { class: "font-mono text-xs px-2 py-1 border-b", "src/{path}" }
            }
            if !language.is_empty() {
                div { class: "font-mono text-xs px-2 py-1 opacity-60", "{language}" }
            }
            pre {
                class: "p-3 overflow-x-auto text-sm",
                code { "{source}" }
            }
        }
    }
}

include!(concat!(env!("OUT_DIR"), "/blog_router.rs"));
