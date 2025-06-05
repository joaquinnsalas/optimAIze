% Magnetostatic force on a charge particle
%--- Arya Menon - Texas A&M
%--Refernce:https://www.mathworks.com/matlabcentral/answers/9120-simulation-of-charged-particle-in-matlab
% magnetostatic_force
function magnetostatic_force
    f=figure(1);
    set(f,'Color',[0.941 0.941 0.941])
    v0_x=0;
    v0_y=0;
    v0_z=0;
    v0 = [v0_x v0_y v0_z]';  %initial velocity
    Bx_new=0;
    By_new=0;
    Bz_new=0;
    B = [Bx_new By_new Bz_new]';  %magnitude of B
    m =5;
    q =1; 
    r0 = [0 0 0]';
    tspan =1;
    % tspan = [0 100];
    y0 = [r0; v0];
    fun=@(t,x) [x(4:6);cross(x(4:6),q/m*B)];
    t=linspace(0,tspan,1e3);
    [t,y]=ode45(fun,t,[r0;v0]);
    

    [fx,fy,fz]=meshgrid(-1:2:1,-1:2:1,-1:2:1);
    ax2=axes('Parent',f,'Position',[0.65 0.05 0.25 0.25]);
    Bx_p=Bx_new*ones(2,2,2);
    By_p=By_new*ones(2,2,2);
    Bz_p=Bz_new*ones(2,2,2);
    demo2=coneplot(ax2,fx,fy,fz,Bx_p,By_p,Bz_p,fx,fy,fz);
    view(-40,18)
    set(demo2,'FaceColor','red','EdgeColor','none')
    set(ax2,'xtick',[])
    set(ax2,'ytick',[])
    set(ax2,'ztick',[])
    light_handle=light('HandleVisibility','on');
    camlight headlight

    material shiny
    set(demo2,'DiffuseStrength',0.8)

    grid on;
    box on;
    light_handle=light('HandleVisibility','off');
    ax1=axes('Parent',f,'Position',[0.1 0.35 0.8 0.6]);
    demo=plot3(ax1,y(:,1),y(:,2),y(:,3),'-b');
    demo1=plot3(ax1,y(1,1),y(1,2),y(1,3),'o','MarkerFaceColor','r');
    view(-40,18)
    grid on;
    box on;

    

    grid on;
    box on;
    t=linspace(0,tspan,1e3);
    
    uicontrol('Style','text','string','x axis',...
     'units','normalized','position',[0.85 0.37 0.1 0.05],...
     'FontSize',12,'FontWeight','Bold' );
     uicontrol('Style','text','string','y axis',...
     'units','normalized','position',[0.08 0.37 0.1 0.05],...
     'FontSize',12,'FontWeight','Bold' );

    
    uicontrol('Style','text','string','B =',...
     'units','normalized','position',[0.1 0.15 0.05 0.05],...
     'FontSize',12,'FontWeight','Bold' );
 

 

    hx = uicontrol(...
            'parent'  , f,...        
            'units'   , 'normalized',...    
            'style'   , 'edit',...        
            'position', [0.2 0.15 0.05 0.05],...
            'callback',@bx,...
            'String',Bx_new);
    hy = uicontrol(...
        'parent'  , f,...        
        'units'   , 'normalized',...    
        'style'   , 'edit',...        
        'position', [0.3 0.15 0.05 0.05],...
        'callback',@by,...
        'String',By_new);
    hz = uicontrol(...
        'parent'  , f,...        
        'units'   , 'normalized',...    
        'style'   , 'edit',...        
        'position', [0.4 0.15 0.05 0.05],...
        'callback',@bz,...
        'String',Bz_new);
    stop=0;
    btn = uicontrol('Parent',f,'Style', 'pushbutton', ...  
        'String', 'Stop',...
        'units','normalized',...
            'Position', [0.925 0.925 0.05 0.05],...
            'Callback', @stop_data);

        uicontrol('Style','text','string','v =',...
     'units','normalized','position',[0.1 0.075 0.05 0.05],...
     'FontSize',12,'FontWeight','Bold' );
 
     uicontrol('Style','text','string','e_x',...
     'units','normalized','position',[0.175 0.2 0.1 0.05],...
     'FontSize',12,'FontWeight','Bold' );
    uicontrol('Style','text','string','e_y',...
     'units','normalized','position',[0.275 0.2 0.1 0.05],...
     'FontSize',12,'FontWeight','Bold' );
     uicontrol('Style','text','string','e_z',...
     'units','normalized','position',[0.375 0.2 0.1 0.05],...
     'FontSize',12,'FontWeight','Bold' );
 
      uicontrol('Style','text','string','Texas A&M University - ECEN 322 - Arya Menon ',...
     'units','normalized','position',[0.001 0.001 0.5 0.05],...
     'FontSize',8);
 

    vx = uicontrol(...
            'parent'  , f,...        
            'units'   , 'normalized',...    
            'style'   , 'edit',...        
            'position', [0.2 0.075 0.05 0.05],...
            'callback',@v0x,...
            'String',v0_x);
    vy = uicontrol(...
        'parent'  , f,...        
        'units'   , 'normalized',...    
        'style'   , 'edit',...        
        'position', [0.3 0.075 0.05 0.05],...
        'callback',@v0y,...
        'String',v0_y);
    vz = uicontrol(...
        'parent'  , f,...        
        'units'   , 'normalized',...    
        'style'   , 'edit',...        
        'position', [0.4 0.075 0.05 0.05],...
        'callback',@v0z,...
        'String',v0_z);

 
   while ~isequal(stop,1)
        flag=0;
        v0 = [v0_x v0_y v0_z]'; 
        y0 = [r0; v0];
        fun=@(t,x) [x(4:6);cross(x(4:6),q/m*B)];
        B=[Bx_new By_new Bz_new]';
        t=linspace(0,tspan,1e3);
        [t,y]=ode45(fun,t,[r0;v0]);
        demo=plot3(ax1,y(:,1),y(:,2),y(:,3),'-b','LineWidth',2);

        view(-40,18)
        
        grid on;
        box on;
        hold on
        demo1=plot3(ax1,y(length(y(:,1)),1),y(length(y(:,1)),2),y(length(y(:,1)),3),...
            'o','MarkerSize',10,'MarkerFaceColor','r');
        grid on;
        box on;
        
        
        Bx_p=Bx_new*ones(2,2,2);
        By_p=By_new*ones(2,2,2);
        Bz_p=Bz_new*ones(2,2,2);
        demo2=coneplot(ax2,fx,fy,fz,Bx_p,By_p,Bz_p,fx,fy,fz);
        view(-40,18)
        set(demo2,'FaceColor','red','EdgeColor','none')
        set(ax2,'xtick',[],'ytick',[],'ztick',[])
        light_handle=light('HandleVisibility','on');
        set(demo2,'FaceLighting','gouraud')
        material shiny
        set(demo2,'DiffuseStrength',0.8)
        camlight left
        lighting gouraud
  
        grid on;
        box on;
        
        pause(0.1);
        light_handle=light('HandleVisibility','off');
        clear light_handle


        if flag==0
        delete(demo1);
 
        end

        tspan=tspan+1;

        
    end
    
    function bx(~,~)
        Bx_new=(str2num(get(hx,'String')));

        cla(ax1);
        cla(ax2);
        
        flag=1;
        tspan=1;
    end
    function by(~,~)
        By_new=(str2num(get(hy,'String')));
        cla(ax1);
        cla(ax2);
        
        flag=1;
        tspan=1;
    end
    function bz(~,~)
        Bz_new=(str2num(get(hz,'String')));
        cla(ax1);
        cla(ax2);
        flag=1;
        tspan=1;
    end
    function v0x(~,~)
        v0_x=str2num(get(vx,'String'));
        cla(ax1);
        cla(ax2);
        
        flag=1;
        tspan=1;
    end
    function v0y(~,~)
        v0_y=str2num(get(vy,'String'));
        cla(ax1);
        cla(ax2);
        
        flag=1;
        tspan=1;
    end
    function v0z(~,~)
        v0_z=str2num(get(vz,'String'));
        cla(ax1);
        cla(ax2);
        
        flag=1;
        tspan=1;
    end
        function stop_data(~,~)
        stop=1;
        end
end