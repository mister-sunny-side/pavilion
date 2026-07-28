use dioxus::prelude::*;

const HELLO_MD: &str = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/pages/hello.md"));

/// Landing page at `/`, content from `pages/hello.md`.
#[component]
pub fn Hello() -> Element {
    let (title, paragraphs) = parse_title_and_paragraphs(HELLO_MD);

    rsx! {
        div {
            id: "hello",
            class: "page page-center",
            h1 { "{title}" }
            for paragraph in paragraphs.iter().copied() {
                p { "{paragraph}" }
            }
        }
    }
}

/// Pull a leading `# Title` and the remaining paragraphs from a markdown file.
fn parse_title_and_paragraphs(md: &'static str) -> (&'static str, Vec<&'static str>) {
    let md = md.trim();
    let (title, body) = if let Some(after_hash) = md.strip_prefix("# ") {
        match after_hash.split_once('\n') {
            Some((title, rest)) => (title.trim(), rest.trim()),
            None => (after_hash.trim(), ""),
        }
    } else {
        ("Hello", md)
    };

    let paragraphs = if body.is_empty() {
        Vec::new()
    } else {
        body.split("\n\n")
            .map(str::trim)
            .filter(|paragraph| !paragraph.is_empty())
            .collect()
    };

    (title, paragraphs)
}
