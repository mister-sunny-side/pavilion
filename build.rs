use std::path::PathBuf;

fn main() {
    println!("cargo:rerun-if-changed=blog-posts");

    let mdbook_dir = PathBuf::from("blog-posts");
    let generated = mdbook_gen::generate_router_build_script(mdbook_dir);
    let out_dir = PathBuf::from(std::env::var("OUT_DIR").expect("OUT_DIR"));
    let dest = out_dir.join("blog_router.rs");

    std::fs::write(&dest, generated).expect("write blog_router.rs");
}
