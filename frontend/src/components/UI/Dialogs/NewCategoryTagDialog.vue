<template>
  <div>
    <v-btn icon @click="dialog = true" class="mt-n1">
      <v-icon :color="color">mdi-plus</v-icon>
    </v-btn>
    <v-dialog v-model="dialog" width="500">
      <v-card>
        <v-app-bar dense dark color="primary mb-2">
          <v-icon large left class="mt-1">
            mdi-tag
          </v-icon>

          <v-toolbar-title class="headline">
            {{ title }}
          </v-toolbar-title>

          <v-spacer></v-spacer>
        </v-app-bar>
        <v-card-title> </v-card-title>
        <v-form @submit.prevent="select">
          <v-card-text>
            <v-text-field
              dense
              :label="inputLabel"
              v-model="itemName"
              :rules="[rules.required]"
            ></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="grey" text @click="dialog = false">
              {{ $t("general.cancel") }}
            </v-btn>
            <v-btn color="success" text type="submit" :disabled="!itemName">
              {{ $t("general.create") }}
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { api } from "@/api";
const CREATED_ITEM_EVENT = "created-item";
export default {
  props: {
    buttonText: String,
    value: String,
    color: {
      default: null,
    },
    tagDialog: {
      default: true,
    },
  },
  data() {
    return {
      dialog: false,
      itemName: "",
      rules: {
        required: val => !!val || "A Name is Required",
      },
    };
  },

  computed: {
    title() {
      return this.tagDialog ? "Create a Tag" : "Create a Category";
    },
    inputLabel() {
      return this.tagDialog ? "Tag Name" : "Category Name";
    },
  },
  watch: {
    dialog(val) {
      if (!val) this.itemName = "";
    },
  },

  methods: {
    async select() {
      const newItem = await (async () => {
        if (this.tagDialog) {
          const newItem = await api.tags.create(this.itemName);
          return newItem;
        } else {
          const newItem = await api.categories.create(this.itemName);
          return newItem;
        }
      })();

      this.$emit(CREATED_ITEM_EVENT, newItem);
      this.dialog = false;
    },
  },
};
</script>

<style>
</style>