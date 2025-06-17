<script setup lang="ts">
import Card from "primevue/card";
import Avatar from "primevue/avatar";
import Fieldset from "primevue/fieldset";
import Panel from "primevue/panel";
import { Button, useToast } from "primevue";
import { computed } from "vue";
import getBackgroundColor from "@/util/usernameBgColor";
import type { Discussion } from "@/api/discussion";
import baseApiUrl from "@/api/baseUrl";
const props = defineProps<Discussion>();
const emit = defineEmits(["delete"]);
const toast = useToast();

const backgroundColor = computed(() => getBackgroundColor(props.author_name));
async function deleteComment() {
  let res = await fetch(new URL(`discussions/${props.id}`, baseApiUrl), {
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
          <div class="user-identify">
            <Avatar
              :label="author_name.charAt(0).toUpperCase()"
              :style="{ backgroundColor }"
            />
            <span>{{ author_name }}</span>
          </div>
        </template>
        <template #icons>
          <Button
            severity="danger"
            icon="pi pi-trash"
            rounded
            text
            @click="deleteComment"
          />
        </template>
        <div v-html="content" />
        <!-- 回复 -->
        <Fieldset v-if="reply_count > 0">
          <template #legend>
            <div class="user-identify">
              <Avatar
                :label="author_name.charAt(0).toUpperCase()"
                :style="{ backgroundColor }"
              />
              <span>{{ author_name }}</span>
            </div>
          </template>
          <div v-html="content" />
        </Fieldset>
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
</style>
