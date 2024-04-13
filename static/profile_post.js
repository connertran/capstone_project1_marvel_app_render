$(".post-delete-btn").click(deletePost);

async function deletePost() {
  try {
    let id = $(this).data("id");
    await axios.delete(`/api/posts/${id}`);
    $(this).closest(".post-div").remove();
  } catch (error) {
    console.error("Error liking/unliking post:", error);
  }
}
