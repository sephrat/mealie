<template>
  <v-card :loading="loading">
    <v-card-title> {{ $t("settings.backup.create-heading") }} </v-card-title>
    <v-card-text class="mt-n3">
      <v-text-field
        dense
        :label="$t('settings.backup.backup-tag')"
        v-model="tag"
      ></v-text-field>
    </v-card-text>
    <v-card-actions class="mt-n9 flex-wrap">
      <v-switch v-model="fullBackup" :label="switchLabel"></v-switch>
      <v-spacer></v-spacer>
      <v-btn color="success" text @click="createBackup()">
        {{ $t("general.create") }}
      </v-btn>
    </v-card-actions>
    <v-expand-transition>
      <div v-if="!fullBackup">
        <v-card-text class="mt-n4">
          <v-row>
            <v-col sm="4">
              <p>{{ $t("general.options") }}:</p>
              <ImportOptions @update-options="updateOptions" class="mt-5" />
            </v-col>
            <v-col>
              <p>{{ $t("general.templates") }}:</p>
              <v-checkbox
                v-for="template in availableTemplates"
                :key="template"
                class="mb-n4 mt-n3"
                dense
                :label="template"
                @click="appendTemplate(template)"
              ></v-checkbox>
            </v-col>
          </v-row>
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script>
import ImportOptions from "@/components/Admin/Backup/ImportOptions";
import { api } from "@/api";
export default {
  components: { ImportOptions },
  data() {
    return {
      tag: null,
      fullBackup: true,
      loading: false,
      options: {
        recipes: true,
        settings: true,
        themes: true,
        users: true,
        groups: true,
      },
      availableTemplates: [],
      selectedTemplates: [],
    };
  },
  mounted() {
    this.getAvailableBackups();
  },
  computed: {
    switchLabel() {
      if (this.fullBackup) {
        return this.$t("settings.backup.full-backup");
      } else return this.$t("settings.backup.partial-backup");
    },
  },
  methods: {
    updateOptions(options) {
      this.options = options;
    },
    async getAvailableBackups() {
      let response = await api.backups.requestAvailable();
      response.templates.forEach(element => {
        this.availableTemplates.push(element);
      });
    },
    async createBackup() {
      this.loading = true;

      let data = {
        tag: this.tag,
        options: {
          recipes: this.options.recipes,
          settings: this.options.settings,
          themes: this.options.themes,
          users: this.options.users,
          groups: this.options.groups,
        },
        templates: this.selectedTemplates,
      };

      await api.backups.create(data);
      this.loading = false;

      this.$emit("created");
    },
    appendTemplate(templateName) {
      if (this.selectedTemplates.includes(templateName)) {
        let index = this.selectedTemplates.indexOf(templateName);
        if (index !== -1) {
          this.selectedTemplates.splice(index, 1);
        }
      } else this.selectedTemplates.push(templateName);
    },
  },
};
</script>

<style>
</style>