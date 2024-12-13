<script setup lang="ts" generic="T">
import { toRefs } from "vue";
import {
  ChevronUpDownIcon,
  ChevronUpIcon,
  ChevronDownIcon,
} from "@heroicons/vue/24/outline";

export type TableCardSlot<T> =
  | {
      isFormRow: true;
    }
  | {
      isFormRow: false;
      data: T;
    };

export type Column = {
  name: string;
  display: string;
  ordering?: boolean;
};

export type Ordering = {
  name: string;
  order: "ascending" | "descending";
};

const props = defineProps<{
  columns: Column[];
  rows: readonly T[];
  extraFormRow?: {
    formName: string;
    formSubmit: () => boolean | Promise<boolean>;
  };
}>();

const ordering = defineModel<Ordering>("ordering");

const { columns, rows, extraFormRow } = toRefs(props);

function setOrdering(column: string) {
  if (ordering?.value?.name === column) {
    if (ordering.value.order === "ascending") {
      ordering.value = {
        name: column,
        order: "descending",
      };
    } else {
      ordering.value = undefined;
    }
  } else {
    ordering.value = {
      name: column,
      order: "ascending",
    };
  }
}
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
            <div
              v-if="column.ordering === true"
              class="flex w-full flex-row justify-center"
            >
              <button
                class="flex flex-row justify-center space-x-1"
                @click="setOrdering(column.name)"
              >
                <span>{{ column.display }}</span>
                <ChevronUpDownIcon
                  v-if="ordering?.name !== column.name"
                  class="w-[24px]"
                />
                <ChevronUpIcon
                  v-else-if="ordering.order === 'ascending'"
                  class="w-[24px]"
                />
                <ChevronDownIcon v-else class="w-[24px]" />
              </button>
            </div>
            <span v-else>{{ column.display }}</span>
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
