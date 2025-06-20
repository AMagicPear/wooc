<script setup lang="ts">
import Card from "primevue/card";
import Fieldset from "primevue/fieldset";
import Panel from "primevue/panel";
import { Button, useToast } from "primevue";
import { onMounted, ref } from "vue";
import type { Discussion, Reply } from "@/api/discussion";
import baseApiUrl from "@/api/baseUrl";
import { accountState } from "@/global/account";
import FloatLabel from "primevue/floatlabel";
import InputText from "primevue/inputtext";
import { Form, type FormSubmitEvent } from "@primevue/forms";
import UserIdentity from "./UserIdentity.vue";

const discussion = defineProps<Discussion>();
const emit = defineEmits(["delete"]);
const toast = useToast();
const showReplyInput = ref<boolean>(false);

async function deleteComment() {
  let res = await fetch(new URL(`/discussions/${discussion.id}`, baseApiUrl), {
    method: "DELETE",
  });
  let result = await res.json();
  if (result) {
    toast.add({
      summary: "话题删除成功",
      severity: "success",
      life: 3000,
    });
    emit("delete");
  } else {
    toast.add({ summary: "删除失败", severity: "error" });
  }
}

const deleteReply = async (id: number) => {
  let res = await fetch(new URL(`/discussion_replies/${id}`, baseApiUrl), {
    method: "DELETE",
  });
  let data = await res.json();
  if (data.result) {
    toast.add({
      summary: "回复删除成功",
      severity: "success",
      life: 3000,
    });
    fetchReplies();
  } else {
    toast.add({
      summary: "回复删除失败",
      detail: data.message,
      severity: "error",
      life: 3000,
    });
  }
};

const fetchReplies = async () => {
  let res = await fetch(
    new URL(`/discussions/${discussion.id}/replies`, baseApiUrl)
  );
  let data = await res.json();
  if (data.result) {
    replies.value = data.replies;
  } else {
    console.error("加载回复失败", data.message);
  }
};

const replies = ref<Reply[]>();
onMounted(() => {
  fetchReplies();
});

const toggleReply = (event: MouseEvent) => {
  showReplyInput.value = !showReplyInput.value;
};

const replySubmit = async (event: FormSubmitEvent) => {
  let content = event.values.reply as string;
  if (!content || content.trim() == "") {
    toast.add({ summary: "回复内容不能为空", severity: "warn" });
    return;
  }
  let res = await fetch(
    new URL(`/discussions/${discussion.id}/replies`, baseApiUrl),
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        author_id: accountState.userid,
        content,
      }),
    }
  );
  let data = await res.json();
  if (data.result) {
    toast.add({
      summary: "回复成功",
      detail: data.message,
      severity: "success",
      life: 3000,
    });
    event.reset();
    fetchReplies();
  } else {
    toast.add({
      summary: "回复失败",
      detail: data.message,
      severity: "error",
      life: 3000,
    });
  }
};
</script>

<template>
  <Card>
    <template #title>
      {{ title
      }}<span v-if="reply_count > 0" style="color: gray">
        ({{ reply_count }}条回复)</span
      ></template
    >
    <template #content>
      <Panel toggleable>
        <template #header>
          <UserIdentity :author_name="author_name" />
        </template>
        <template #icons>
          <Button
            severity="secondary"
            icon="pi pi-reply"
            rounded
            text
            v-on:click="toggleReply"
          />
          <Button
            severity="danger"
            icon="pi pi-trash"
            rounded
            text
            @click="deleteComment"
            v-if="author_id == accountState.userid"
          />
        </template>
        <div v-html="content" />
        <!-- 回复 -->
        <Fieldset v-for="reply in replies">
          <template #legend>
            <UserIdentity :author_name="reply.author_name"/>
          </template>

          <div
            style="
              display: flex;
              justify-content: space-between;
            "
          >
            <div v-html="reply.content" />
            <Button
              severity="danger"
              icon="pi pi-trash"
              rounded
              text
              @click="deleteReply(reply.id)"
              style="flex-shrink: 0"
              v-if="reply.author_id == accountState.userid"
            />
          </div>
        </Fieldset>

        <Transition>
          <Form
            v-show="showReplyInput"
            :action="`${baseApiUrl}/discussions/${discussion.id}/replies`"
            method="POST"
            @submit="replySubmit($event)"
          >
            <FloatLabel
              variant="on"
              style="display: flex; gap: 1rem; margin-top: 1rem"
            >
              <InputText
                name="reply"
                id="reply"
                autocomplete="off"
                style="flex-grow: 7"
              />
              <label for="reply">在此输入回复</label>
              <Button type="submit" label="发送" style="flex-grow: 3"></Button>
            </FloatLabel>
          </Form>
        </Transition>
      </Panel>
    </template>
  </Card>
</template>

<style lang="css" scoped>
.user-identify {
  display: flex;
  align-items: center;
  padding-left: 0.5rem;
  gap: 0.5rem;
}

.lengend-text {
  font-weight: bold;
  padding: 0.5rem;
}

.fieldset-content {
  margin: 0;
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
