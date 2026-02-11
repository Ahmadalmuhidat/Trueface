import customtkinter
from typing import List, Callable, Any

class PaginationComponent:
  def __init__(self, parent, items_per_page: int = 50, on_page_change: Callable = None) -> None:
    self.parent = parent
    self.items_per_page = items_per_page
    self.on_page_change = on_page_change
    
    self.current_page = 1
    self.total_items = 0
    self.total_pages = 0
    self.data = []
    
    self.pagination_frame = None
    self.page_info_label = None
    self.prev_button = None
    self.next_button = None
    
    self._create_pagination_ui()
  
  def _create_pagination_ui(self) -> None:
    self.pagination_frame = customtkinter.CTkFrame(
      self.parent,
      fg_color="transparent"
    )
    
    content_frame = customtkinter.CTkFrame(
      self.pagination_frame,
      fg_color="transparent"
    )
    content_frame.pack(expand=True)
    
    nav_frame = customtkinter.CTkFrame(
      content_frame,
      fg_color="transparent"
    )
    nav_frame.pack(pady=2)
    
    self.prev_button = customtkinter.CTkButton(
      nav_frame,
      text="Previous",
      width=60,
      height=25,
      command=self._go_to_previous_page,
      state="disabled"
    )
    self.prev_button.pack(side="left", padx=3)
    
    self.next_button = customtkinter.CTkButton(
      nav_frame,
      text="Next",
      width=60,
      height=25,
      command=self._go_to_next_page,
      state="disabled"
    )
    self.next_button.pack(side="left", padx=3)
  
  def set_data(self, data: List[Any]) -> None:
    self.data = data
    self.total_items = len(data)
    self.total_pages = max(1, (self.total_items + self.items_per_page - 1) // self.items_per_page)
    self.current_page = min(self.current_page, self.total_pages)
    self._update_pagination_ui()
    self._notify_page_change()
  
  def get_current_page_data(self) -> List[Any]:
    if not self.data:
      return []
    
    start_index = (self.current_page - 1) * self.items_per_page
    end_index = start_index + self.items_per_page
    return self.data[start_index:end_index]
  
  def _update_pagination_ui(self) -> None:
    self.prev_button.configure(state="normal" if self.current_page > 1 else "disabled")
    self.next_button.configure(state="normal" if self.current_page < self.total_pages else "disabled")
  
  def _go_to_previous_page(self) -> None:
    if self.current_page > 1:
      self.current_page -= 1
      self._update_pagination_ui()
      self._notify_page_change()
  
  def _go_to_next_page(self) -> None:
    if self.current_page < self.total_pages:
      self.current_page += 1
      self._update_pagination_ui()
      self._notify_page_change()
  
  def _notify_page_change(self) -> None:
    if self.on_page_change:
      self.on_page_change(self.get_current_page_data(), self.current_page)
  
  def pack(self, **kwargs) -> None:
    self.pagination_frame.pack(**kwargs)
  
  def grid(self, **kwargs) -> None:
    self.pagination_frame.grid(**kwargs)
  
  def get_pagination_info(self) -> dict:
    return {
      "current_page": self.current_page,
      "total_pages": self.total_pages,
      "total_items": self.total_items,
      "items_per_page": self.items_per_page,
      "start_index": (self.current_page - 1) * self.items_per_page + 1 if self.total_items > 0 else 0,
      "end_index": min(self.current_page * self.items_per_page, self.total_items)
    }
  
  def destroy(self) -> None:
    if self.pagination_frame:
      try:
        for child in self.pagination_frame.winfo_children():
          if hasattr(child, 'destroy'):
            child.destroy()
      except Exception as e:
        pass
      
      self.pagination_frame.destroy()
      self.pagination_frame = None
      
      self.page_info_label = None
      self.prev_button = None
      self.next_button = None
