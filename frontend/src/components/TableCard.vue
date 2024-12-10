<script setup lang="ts" generic="T">
import { toRefs } from "vue";

export type TableCardSlot<T> =
  | {
      isFormRow: true;
    }
  | {
      isFormRow: false;
      data: T;
    };

const props = defineProps<{
  columns: readonly { name: string; display: string }[];
  rows: readonly T[];
  extraFormRow?: {
    formName: string;
    formSubmit: () => boolean | Promise<boolean>;
  };
}>();

// defineSlots;

const { columns, rows, extraFormRow } = toRefs(props);
</script>

<template>
  <div
    class="mt-4 rounded-3xl bg-slate-100 px-0 py-6 text-surface-content-light shadow-md dark:bg-secondary-dark dark:text-surface-content-dark"
  >
    <form
      v-if="extraFormRow !== undefined"
      :id="extraFormRow.formName"
      @submit.prevent="extraFormRow.formSubmit"
    />

    <table
      class="w-full table-auto bg-slate-100 text-center dark:bg-secondary-dark"
    >
      <thead
        class="border-b border-secondary-light dark:border-secondary-active-dark"
      >
        <tr>
          <th v-for="column in columns" v-bind:key="column.name" class="py-2">
            {{ column.display }}
          </th>
        </tr>
      </thead>
      <tbody class="bg-surface-light dark:bg-surface-dark">
        <tr v-for="[rowIndex, row] in rows.entries()" v-bind:key="rowIndex">
          <td
            v-for="column in columns"
            v-bind:key="column.name"
            class="border-b border-secondary-light py-4 dark:border-secondary-active-dark"
          >
            <slot
              :name="column.name"
              v-bind="{ isFormRow: false, data: row } as TableCardSlot<T>"
            ></slot>
          </td>
        </tr>
        <tr>
          <td
            v-for="column in columns"
            v-bind:key="column.name"
            class="border-b border-secondary-light py-4 dark:border-secondary-active-dark"
          >
            <slot
              :name="column.name"
              v-bind="{ isFormRow: true } as TableCardSlot<T>"
            ></slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
