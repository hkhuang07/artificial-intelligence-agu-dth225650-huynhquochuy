#include <stdio.h>
#include <conio.h>
#include <stdbool.h>
#define MAX 100

int a[MAX][MAX];  //mảng 2 chiều đại diện cho dữ liệu đầu vào
int n;            //Số đỉnh/ cặp
_Bool visit[MAX]; //Mảng 1 chiều các giá trị bool đã/ chưa ghé qua
int queue[MAX];   //Mảng 1 chiều các giá trị trong hàng đợi

//Hàm hiển thị mảng 2 chiểu có MAX hàng MAX cột
void show(int a[MAX][MAX])
{
   int i,j;
   putchar('\n');
   for (i=0;i<n;i++,putchar('\n'))
      for (j=0;j<n;j++)
         printf(" %2d ", a[i][j]);
}

//Hàm khời tạo 
void init(char *fname)
{
   //Mở file, đọc và hiển thị giá trị đỉnh
   FILE *f;
   f = fopen(fname,"r"); //Mở file dữ liệu để đọc
   printf( !f ? "\n File Cannot Read!!!" : "\n Read File Successfully!!!\n"); //Thông báo mở thành công/ thất bại
   fscanf(f,"%d",&n);   //Read giá trị số đỉnh n trong file
   printf("%d\n",n);    //In số đỉnh 

   //Duyệt mảng 2 chiều
   int i,j;
   for (i=0;i<n;i++)    // mỗi hàng
      for (j=0;j<n;j++) // mỗi cột
         fscanf(f,"%d",&a[i][j]);  //Read giá trị trong mảng 2 chiều

   show(a); //Hiển thị mảng
   getchar();
   fclose(f); 
}

//Giải thuật Breath First Search
void bfs(int start)
{
   int top, bottom, k, v; //khai báo biến
   top=bottom=1;           
   visit[start]=true;      //Duyệt qua giá trị start
   queue[bottom++]=start;  //cho giá trị start vào hàng đợi (Như Open list của các giải thuật khác)
   while(top!=bottom) //trong khi top khác bottom
   {
      v=queue[top++];        //cập nhật mảng v thành hàng đợi hiện tại chứ các giá trị đỉnh đã duyệt
      printf(" %2d ", v+1); // in mảng v các giá trị đã duyệt
      getchar();
      for (k=0;k<n;k++)  
      {
         if (a[v][k]!=0 && !visit[k]) //nếu giá trị xét tiếp theo trong mảng 2 chiều khác 0 và chưa được duyệt thì...
         {
            queue[bottom++]=k;  //thêm đỉnh này vào danh sách hàng đợi để duyệt 
            visit[k]=true;      //Gán cho đỉnh này đã được duyệt
         }
      } 	
   }
}

void traverse()
{
   int i,j;
   for (i=0;i<n;i++)  
      visit[i]=false;  //Thiết lập đánh dấu chưa duyệt cho mảng 2 chiều
   for (i=0;i<n;i++)    //duyệt mảng 2 chiều, nếu đỉnh chưa duyệt thì duyệt BFS
      if (!visit[i])
         bfs(i);
}

int main()
{
   init("bfs.txt");
   traverse();
   getchar();
   return 0;
}
