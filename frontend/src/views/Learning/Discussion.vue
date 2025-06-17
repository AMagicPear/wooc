<script setup lang="ts">
import Card from "primevue/card";
import Editor from "primevue/editor";
import { Button } from "primevue";
import { Form } from "@primevue/forms";
import { onMounted, ref } from "vue";
import CommentCard from "@/components/CommentCard.vue";
import { accountState } from "@/global/account";
import type { Discussion, DiscussionPost } from "@/api/discussion";
import { useRoute } from "vue-router";
import baseApiUrl from "@/api/baseUrl";

const editorValue = ref<string>();
const courseId = Number(useRoute().params.id);
const discussions = ref<Discussion[]>()
const onDiscussionSubmit = () => {
  let discussion: DiscussionPost | undefined = undefined;
  if (editorValue.value) {
    discussion = {
      course_id: courseId,
      title: "",
      content: editorValue.value,
      author_id: accountState.userid,
    };
  }
  console.log(discussion);
};

onMounted(async () => {
  let res = await fetch(new URL(`courses/${courseId}/discussions`, baseApiUrl));
  let allDiscussion = await res.json();
  if (allDiscussion.result) {
    discussions.value = allDiscussion.discussions as Discussion[]
  } else {
    console.error(allDiscussion.message);
  }
});

</script>

<template>
  <div id="discussion">
    <Card>
      <template #title>讨论区</template>
      <template #content>
        <p>
          欢迎大家来到讨论区！本讨论区供各位同学就课程问题进行交流学习。请同学们认真阅读下面的【讨论区使用规则】，然后再进行相关发表，谢谢！
        </p>
        <Form @submit="onDiscussionSubmit" class="discussion-form">
          <Editor
            name="content"
            v-model="editorValue"
            editorStyle="height: 120px"
          />
          <Button type="submit" severity="secondary" label="发表评论" />
        </Form>
      </template>
    </Card>
    <CommentCard v-for="discussion in discussions" :username="discussion.author_name" :content="discussion.content" :title="discussion.title"/>
    <CommentCard v-for="discussion in discussions" :username="discussion.author_name" :content="discussion.content" :title="discussion.title"/>
  </div>
</template>

<style lang="css" scoped>
#discussion {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-bottom: 20px;
}

.discussion-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
