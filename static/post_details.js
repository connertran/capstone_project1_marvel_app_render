// for likes
$(".like-unlike").click(likeUnlikePost);

async function likeUnlikePost() {
  try {
    let post_id = $(this).data("id");
    let $icon = $(this).find("i");
    if ($icon.hasClass("fa-regular fa-thumbs-up")) {
      await axios.post(`/api/posts/${post_id}/like`);
      $icon
        .removeClass("fa-regular fa-thumbs-up")
        .addClass("fa-solid fa-thumbs-up");
    } else if ($icon.hasClass("fa-solid fa-thumbs-up")) {
      await axios.delete(`/api/posts/${post_id}/like`);
      $icon
        .removeClass("fa-solid fa-thumbs-up")
        .addClass("fa-regular fa-thumbs-up");
    }
  } catch (error) {
    console.error("Error liking/unliking post:", error);
  }
}

//for comments
function friendlyDate(timestamp) {
  const date = new Date(timestamp);

  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  const dayOfWeek = days[date.getDay()];
  const month = months[date.getMonth()];
  const dayOfMonth = date.getDate();
  const year = date.getFullYear();
  let hours = date.getHours();
  const minutes = date.getMinutes();
  const ampm = hours >= 12 ? "PM" : "AM";
  hours = hours % 12 || 12; // Convert 0 to 12 for midnight

  const friendlyDateStr = `${dayOfWeek} ${month} ${dayOfMonth} ${year}, ${hours}:${minutes
    .toString()
    .padStart(2, "0")} ${ampm}`;

  return friendlyDateStr;
}

$(".comment-post-btn").click(addComment);

async function addComment(evt) {
  evt.preventDefault();
  try {
    let post_id = $(this).data("id");
    const commentText = $(".comment").val();

    let resp = await axios.post(`/api/posts/${post_id}/comments`, {
      text: commentText,
    });

    const comment = resp.data.comment;
    $(".comment-section").append(`
    <div class="comment-div">
      <p>${comment.user_id}</p>
      <p>${comment.text}</p>
      <p>${friendlyDate(comment.timestamp)}</p>
    </div>
    `);
    $(".comment").val("");
  } catch (error) {
    console.error("Error adding comment:", error);
  }
}
